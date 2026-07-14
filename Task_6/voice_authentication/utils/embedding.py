import torch
import torch.nn.functional as F
import config
from models.model import ECAPATDNN
from utils.preprocessing import preprocess_audio

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model():

    try:
        model = ECAPATDNN(num_speakers=config.NUM_SPEAKERS)

        state_dict = torch.load(config.MODEL_PATH, map_location=device)

        model.load_state_dict(state_dict)

        model.to(device)

        model.eval()
        print("ECAPA-TDNN model loaded successfully.")

        return model

    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found {config.MODEL_PATH}")

    except RuntimeError as e:
        raise RuntimeError(f"Failed to load model weight \n{e} ")

    except Exception as e:
        raise Exception(f"Unexpected error while loading model.\n{e}")


model = load_model()


def generate_embedding(file_path):

    mel = preprocess_audio(file_path)
    mel = mel.squeeze(0)
    mel = mel.unsqueeze(0)
    mel = mel.transpose(1, 2)
    mel = mel.to(device)

    with torch.no_grad():
        _, embedding = model(mel)

    embedding = F.normalize(embedding, p=2, dim=1)

    return embedding.cpu()
