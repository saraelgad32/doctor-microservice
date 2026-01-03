import grpc
from concurrent import futures
import time
import doctor_pb2
import doctor_pb2_grpc
import pyodbc
import config

# --- CONFIGURATION ---
SERVER_NAME = 'SARAHP414'
DATABASE_NAME = 'DoctorServiceDB'

class DoctorService(doctor_pb2_grpc.DoctorControllerServicer):
    def GetDoctors(self, request, context):
        # 1. Debug Print (This lets you see what Django sent)
        print(f"\n--- REQUEST RECEIVED: '{request.neighborhood}' ---")
        
        doctors_list = []
        try:
            print(f"Connecting to {SERVER_NAME}...")
            conn_str = (
                        f'DRIVER={config.DB_CONFIG["driver"]};'
                        f'SERVER={config.DB_CONFIG["server"]};'
                        f'DATABASE={config.DB_CONFIG["database"]};'
                        f'Trusted_Connection={config.DB_CONFIG["trusted_connection"]};'
            )
            conn = pyodbc.connect(conn_str, timeout=5)
            cursor = conn.cursor()
            
            # --- THE MISSING LOGIC STARTS HERE ---
            
            # Start with the base query
            sql = "SELECT Name, Specialty, Neighborhood, Phone FROM Doctors"
            params = []

            # Check if we need to filter
            if request.neighborhood and request.neighborhood != "" and request.neighborhood != "All":
                print(f"   -> FILTERING APPLIED: {request.neighborhood}")
                sql += " WHERE Neighborhood = ?"
                params.append(request.neighborhood)
            else:
                print("   -> SHOWING EVERYONE (No filter)")

            # Execute with the params
            cursor.execute(sql, params)
            
            # --- THE MISSING LOGIC ENDS HERE ---
            
            rows = cursor.fetchall()
            print(f"Found {len(rows)} doctors.")

            # 3. Pack Data
            for row in rows:
                doc = doctor_pb2.DoctorData(
                    id=0,
                    name=row.Name,
                    specialty=row.Specialty,
                    neighborhood=row.Neighborhood if row.Neighborhood else "Unknown",
                    phone=row.Phone if row.Phone else "N/A"
                )
                doctors_list.append(doc)
            
            conn.close()
            print("Sending data to Django... ✅")

        except Exception as e:
            print(f"!!! ERROR: {e}")
            doctors_list.append(doctor_pb2.DoctorData(name="Error", specialty=str(e)))

        return doctor_pb2.DoctorList(doctors=doctors_list)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    doctor_pb2_grpc.add_DoctorControllerServicer_to_server(DoctorService(), server)
    server.add_insecure_port('[::]:50051')
    print("Microservice is running... (With Phone Support)")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

