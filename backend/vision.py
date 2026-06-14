import cv2
import mediapipe as mp
import numpy as np

class VisionAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Landmark indices for eyes (MediaPipe Face Mesh Refined)
        self.LEFT_IRIS = [468, 469, 470, 471]
        self.RIGHT_IRIS = [473, 474, 475, 476]
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

    def process_frame(self, frame):
        """
        Processes a single frame to calculate eye contact metrics.
        Returns a dictionary with eye contact status and raw metrics.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return {"eye_contact": False, "score": 0.0, "error": "No face detected"}

        face_landmarks = results.multi_face_landmarks[0]
        
        # Simplified Eye Contact Logic:
        # Check if irises are centered within the eye boundaries
        # For the MVP, we calculate the horizontal and vertical ratio of the iris center
        
        l_iris_center = self._get_landmarks_center(face_landmarks, self.LEFT_IRIS)
        r_iris_center = self._get_landmarks_center(face_landmarks, self.RIGHT_IRIS)
        
        # Calculate horizontal gaze (simplistic metric)
        # Ideally, this would be compared against the eye's bounding box
        # For now, we return a score based on the iris presence
        
        return {
            "eye_contact": True,
            "score": 1.0, # Placeholder for more complex calculation
            "iris_coords": {"left": l_iris_center, "right": r_iris_center}
        }

    def _get_landmarks_center(self, landmarks, indices):
        points = []
        for idx in indices:
            lm = landmarks.landmark[idx]
            points.append([lm.x, lm.y])
        return np.mean(points, axis=0).tolist()

    def __del__(self):
        self.face_mesh.close()
