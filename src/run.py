from src.VirtualClassroom import create_app

app, socket_io = create_app()
socket_io.run(app, debug=True)
