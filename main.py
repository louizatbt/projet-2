from website import create_app

app=create_app()

if __name__ == '__main__': #sert a pouvoir importer main.py dans d'autres fichier sans qu'il se lance
    app.run(debug=True)