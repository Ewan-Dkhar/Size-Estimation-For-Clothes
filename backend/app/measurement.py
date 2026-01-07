import numpy as np
import pandas as pd

def extract_features_from_keypoints(keypoints, image_height, image_width, person_height_input):
    # Standard Setup
    kps = np.squeeze(keypoints)
    
    def get_xy(idx):
        y_norm, x_norm, score = kps[idx]
        return np.array([x_norm * image_width, y_norm * image_height]), score

    # Extract Critical Points (Focus on Hips/Shoulders/Knees)
    l_shoulder, s_ls = get_xy(5)
    r_shoulder, s_rs = get_xy(6)
    l_hip, s_lh = get_xy(11)
    r_hip, s_rh = get_xy(12)
    l_knee, s_lk = get_xy(13)
    l_ankle, s_la = get_xy(15)
    
    # Arm points for feature extraction
    l_elbow, _ = get_xy(7)
    l_wrist, _ = get_xy(9)

    # Safety Check: If we can't see the core body, abort
    # We are less strict about eyes now, but we need hips/shoulders/knees
    if min(s_ls, s_rs, s_lh, s_rh, s_lk) < 0.2:
        return None

    # Calculate Raw Pixel Lengths
    # Shoulder Width
    shoulder_px = np.linalg.norm(l_shoulder - r_shoulder)
    
    # Hip Width
    hip_px = np.linalg.norm(l_hip - r_hip)
    
    # Torso (Vertical Centerline)
    mid_shoulder = (l_shoulder + r_shoulder) / 2
    mid_hip = (l_hip + r_hip) / 2
    torso_px = np.linalg.norm(mid_shoulder - mid_hip)
    
    # Leg (Hip -> Knee -> Ankle)
    # If ankle is low confidence, we can estimate lower leg based on upper leg
    upper_leg_px = np.linalg.norm(l_hip - l_knee)
    
    if s_la > 0.2:
        lower_leg_px = np.linalg.norm(l_knee - l_ankle)
    else:
        # Lower leg is usually ~85% of upper leg length
        lower_leg_px = upper_leg_px * 0.85
        
    leg_px = upper_leg_px + lower_leg_px
    
    # Arm
    arm_px = np.linalg.norm(l_shoulder - l_elbow) + np.linalg.norm(l_elbow - l_wrist)

    # NEW HEIGHT ESTIMATION LOGIC
    body_core_px = torso_px + leg_px
    
    # Core body is apprx 82% of full height (Head/Neck is the rest)
    estimated_total_height_px = body_core_px / 0.82
    
    # using my height as of now, later this will we given be the user
    assumed_real_height_cm = person_height_input
    
    scale_factor = assumed_real_height_cm / (estimated_total_height_px + 1e-6)
    
    # Final Features
    features = {
        'shoulder_width_cm': shoulder_px * scale_factor,
        'hip_width_cm': hip_px * scale_factor,
        'torso_length_cm': torso_px * scale_factor,
        'arm_length_cm': arm_px * scale_factor,
        'leg_length_cm': leg_px * scale_factor,
        'torso_leg_ratio': (torso_px) / (leg_px + 0.1)
    }
    
    return pd.DataFrame([features])


