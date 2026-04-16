from app import create_app

app = create_app()

if __name__ == '__main__':
    # 提供預設啟動伺服器的方法，方便開發測試
    app.run(debug=True)
