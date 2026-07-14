# Audio Configuration
SAMPLE_RATE = 16000
N_MELS = 80

N_FFT = 512
WIN_LENGTH = 400
HOP_LENGTH = 160

CROP_DURATION = 3

NUM_SPEAKERS = 100
MODEL_PATH = r"D:\Internship_projects\biome-internship-projects"
r"\Task_6\voice_authentication\models\ecapa_tdnn.pth"

UPLOAD_FOLDER = "uploads"
EMBEDDING_FOLDER = "embeddings"

SIMILARITY_THRESHOLD = 0.75

SECRET_KEY = "voice_auth_secret_key"
ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a"}
