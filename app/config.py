FIELDS = {
    "ProfileName": {"type": "text", "limit": 11},
    "OpMode": {"type": "combo", "choices": [
        "Auto record","Walkin. Protoc.","Road Protocol",
        "Fixed P. Proto.","RhinoLogger","Heterodyne",
        "Timed recording","Audio Rec.","Synchro"
    ]},
    "StartTime": {"type": "text"},
    "EndTime": {"type": "text"},
    "SampFreqU": {"type": "combo", "choices": ["24","48","96","192","250","384","500"]},
    "NumericGain": {"type": "combo", "choices": ["0","6","12","18","24"]},
    "StereoMode": {"type": "combo", "choices": ["Stereo","MonoRight","MonoLeft"]},
    "MicrophoneType": {"type": "combo", "choices": ["SPU0410","ICS40730","FG23329"]},
    "LEDSynchro": {"type": "combo", "choices": ["NO","REC","3 REC"]},
    "WavPrefix": {"type": "text", "limit": 5},
    "MaxFileLength": {"type": "int", "min": 1, "max": 999, "default": 60},
    "MinFreqUS": {"type": "int", "min": 10000, "max": 120000},
    "MaxFreqUS": {"type": "int", "min": 20000, "max": 120000},
    "MinLevel": {"type": "int", "min": 0, "max": 100, "default": 15},
    "PreTrigger": {"type": "int", "min": 0, "max": 10, "default": 5},
    "THSensorEnable": {"type": "combo", "choices": ["0","1"], "default": "1"},
    "GPSenable": {"type": "combo", "choices": ["0","1"], "default": "0"},
}

SECTION_TITLES = {
    "Profil": ["ProfileName", "OpMode"],
    "Horaires": ["StartTime", "EndTime"],
    "Audio": ["SampFreqU", "NumericGain", "StereoMode", "MicrophoneType"],
    "Fichiers": ["LEDSynchro", "WavPrefix", "MaxFileLength"],
    "Fréquences": ["MinFreqUS", "MaxFreqUS", "MinLevel", "PreTrigger"],
    "Capteurs": ["THSensorEnable", "GPSenable"]
}

PROFILE_LABELS = {"Profile 2": "2", "Profile 3": "3", "Profile 4": "4", "Profile 5": "5"}

BUILD_VERSION = "0.2"