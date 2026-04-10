from app import create_app

app = create_app()

if __name__ == "__main__":
    import os

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))

    print("Login URLs:")
    print(f"- User (Donor): http://{host}:{port}/login")
    print(f"- Admin:       http://{host}:{port}/admin/login")

    app.run(debug=True, host=host, port=port)