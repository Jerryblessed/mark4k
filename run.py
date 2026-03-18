from app import create_app, db
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("\n🎓 Mark4k Academic Assistant")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" http://localhost:5000")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    app.run(debug=True)