import cv2
from utils.detector import detect_faces
from utils.encoder import encode_face
from utils.matcher import match_face
from utils.database import load_database


def recognize_video(source=0):
    db = load_database("embeddings/database.pkl")
    cap = cv2.VideoCapture(source)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces(frame)
        for (x, y, w, h), face_img in faces:
            encoding = encode_face(face_img)
            name, confidence = match_face(encoding, db)
            label = f"{name} ({confidence:.2f}%)"
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    recognize_video()