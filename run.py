import uvicorn
import os
        
if __name__ == "__main__":
    # receiveMesasgeTopic()
    # reload ถ้า deploy ไว้บน server ห้าม API reload ตัวเอง
    uvicorn.run(app="main:app", host="0.0.0.0", port=2002, reload=os.environ.get('ENVIRONMENT') != "production")
    