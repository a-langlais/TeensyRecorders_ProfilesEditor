FIELDS = {
    # ---- Profil ----
    "ProfileName": {"type": "text", "limit": 11},
    "OpMode": {"type": "combo", "choices": [
        "Auto record","Walkin. Protoc.","Road Protocol",
        "Fixed P. Proto.","RhinoLogger","Heterodyne",
        "Timed recording","Audio Rec.","Synchro"
    ]},

    # ---- Horaires ----
    "StartTime": {"type": "text"},
    "EndTime": {"type": "text"},
    "RecTime": {"type": "int", "min": 1, "max": 3600, "step": 10, "default": 60},
    "WaitTime": {"type": "int", "min": 1, "max": 3600, "step": 10, "default": 540},

    # ---- Audio ----
    "SampFreqU": {"type": "combo", "choices": ["24","48","96","192","250","384","500"]},
    "SampFreqA": {"type": "combo", "choices": ["24","48","96","192"]},
    "NumericGain": {"type": "combo", "choices": ["0","6","12","18","24"]},
    "LowpassFilter": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "HighpassFilter": {"type": "int", "min": 0, "max": 25, "default": 0},
    "fHighpassFilter": {"type": "float", "min": 0.0, "max": 25.0, "step": 0.1, "default": 0.0},
    "Exp10": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "StereoMode": {"type": "combo", "choices": ["Stereo","MonoRight","MonoLeft"]},
    "MicrophoneType": {"type": "combo", "choices": ["SPU0410","ICS40730","FG23329"]},

    # ---- Hétérodyne ----
    "HeterodyneMode": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "AutoRecHeter": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "RefreshGraphe": {"type": "float", "min": 0.2, "max": 2.0, "step": 0.2, "default": 1.0},
    "HeterLevel": {"type": "float", "min": 0.1, "max": 0.9, "step": 0.1, "default": 0.5},
    "Pre-TriggerAuto": {"type": "int", "min": 0, "max": 10, "default": 1},
    "Pre-TriggerHeter": {"type": "int", "min": 0, "max": 10, "default": 3},
    "HeterSelectiveFilter": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "HeterAutoPlay": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "HeterWithGraph": {"type": "combo", "choices": ["0","1"], "default": "1"},
    "HeterAGC": {"type": "combo", "choices": ["0","1"], "default": "0"},

    # ---- Fichiers ----
    "WavPrefix": {"type": "text", "limit": 5},
    "LEDSynchro": {"type": "combo", "choices": ["NO","REC","3 REC"]},
    "BatcorderMode": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "MaxFileLength": {"type": "int", "min": 1, "max": 999, "default": 60},

    # ---- Fréquences ----
    "MinFreqUS": {"type": "int", "min": 100, "max": 150000, "step": 100},
    "MaxFreqUS": {"type": "int", "min": 100, "max": 150000, "step": 100},
    "MinFreqA": {"type": "int", "min": 100, "max": 96000, "step": 100},
    "MaxFreqA": {"type": "int", "min": 100, "max": 96000, "step": 100},
    "MinDuration": {"type": "int", "min": 1, "max": 99, "default": 1},
    "MaxDuration": {"type": "int", "min": 1, "max": 999, "default": 10},
    "ThresholdType": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "RelativeThreshold": {"type": "int", "min": 5, "max": 99, "default": 18},
    "AbsoluteThreshold": {"type": "int", "min": -110, "max": -30, "default": -90},
    "NbDetect": {"type": "int", "min": 1, "max": 8, "default": 3},
    "MinLevel": {"type": "int", "min": 0, "max": 100, "default": 15},
    "PreTrigger": {"type": "int", "min": 0, "max": 10, "default": 5},

    # ---- Capteurs ----
    "TemperaturePeriod": {"type": "int", "min": 10, "max": 3600, "step": 10, "default": 600},
    "ContMesTemp": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "SaveNoise": {"type": "combo", "choices": ["0","1"], "default": "0"},
    "THSensorEnable": {"type": "combo", "choices": ["0","1"], "default": "1"},
    "GPSenable": {"type": "combo", "choices": ["0","1"], "default": "0"},
}

SECTION_TITLES = {
    "Profil": ["ProfileName", "OpMode"],
    "Fichiers": ["LEDSynchro","WavPrefix","BatcorderMode","MaxFileLength"],
    "Horaires": ["StartTime", "EndTime", "RecTime", "WaitTime"],
    "Fréquences": ["MinFreqUS","MaxFreqUS","MinFreqA","MaxFreqA","MinDuration","MaxDuration","ThresholdType","RelativeThreshold","AbsoluteThreshold","NbDetect", "MinLevel","PreTrigger"],
    "Audio": ["SampFreqU","SampFreqA","NumericGain","LowpassFilter","HighpassFilter","fHighpassFilter","Exp10","StereoMode","MicrophoneType"],
    "Hétérodyne": ["HeterodyneMode","AutoRecHeter","RefreshGraphe","HeterLevel","Pre-TriggerAuto","Pre-TriggerHeter","HeterSelectiveFilter","HeterAutoPlay","HeterWithGraph","HeterAGC"],
    "Autre": ["SaveNoise","THSensorEnable","TemperaturePeriod","ContMesTemp"] # "GPSenable" hidden
}

PROFILE_LABELS = {"Profile 2": "2", "Profile 3": "3", "Profile 4": "4", "Profile 5": "5"}

BUILD_VERSION = "0.3"
