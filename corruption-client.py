import requests
import json
from datetime import datetime
from typing import Optional, Dict, List
import sys
from datetime import datetime

class CorruptionCaseClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_all_cases(self) -> List[Dict]:
        """Mendapatkan semua kasus"""
        response = requests.get(f"{self.base_url}/cases")
        response.raise_for_status()
        return response.json()

    def get_case(self, case_id: int) -> Dict:
        """Mendapatkan detail kasus spesifik"""
        response = requests.get(f"{self.base_url}/cases/{case_id}")
        response.raise_for_status()
        return response.json()

    def get_case_types(self) -> List[str]:
        """Mendapatkan daftar jenis kasus"""
        response = requests.get(f"{self.base_url}/cases/types")
        response.raise_for_status()
        return response.json()

    def create_case(self, case_data: Dict) -> Dict:
        """Membuat kasus baru"""
        response = requests.post(f"{self.base_url}/cases", json=case_data)
        response.raise_for_status()
        return response.json()

    def update_case_status(self, case_id: int, new_status: str, timeline_desc: str) -> Dict:
        """Mengupdate status kasus"""
        params = {"new_status": new_status, "timeline_desc": timeline_desc}
        response = requests.put(f"{self.base_url}/cases/{case_id}", params=params)
        response.raise_for_status()
        return response.json()

    def delete_case(self, case_id: int) -> Dict:
        """Menghapus kasus"""
        response = requests.delete(f"{self.base_url}/cases/{case_id}")
        response.raise_for_status()
        return response.json()

def print_menu():
    """Menampilkan menu utama"""
    print("\n=== Sistem Manajemen Kasus Korupsi ===")
    print("1. Lihat Semua Kasus")
    print("2. Lihat Detail Kasus")
    print("3. Tambah Kasus Baru")
    print("4. Update Status Kasus")
    print("5. Hapus Kasus")
    print("6. Lihat Statistik")
    print("7. Keluar")
    print("=====================================")

def get_case_input() -> Dict:
    """Mendapatkan input data kasus dari pengguna"""
    print("\nMasukkan data kasus baru:")
    case_data = {}
    
    try:
        case_data["year"] = int(input("Tahun (contoh: 2024): "))
        
        print("\nPilih tipe kasus:")
        print("1. Pengadaan (procurement)")
        print("2. Suap (bribery)")
        print("3. Gratifikasi (gratification)")
        print("4. Pencucian Uang (money laundering)")
        
        case_type_map = {
            "1": "pengadaan",
            "2": "suap",
            "3": "gratifikasi",
            "4": "pencucian_uang"
        }
        
        case_type = input("Pilihan (1-4): ")
        case_data["case_type"] = case_type_map[case_type]
        
        case_data["description"] = input("Deskripsi kasus: ")
        case_data["institution"] = input("Nama institusi: ")
        case_data["loss_amount"] = float(input("Jumlah kerugian (dalam rupiah): "))
        
        print("\nPilih status kasus:")
        print("1. Investigasi")
        print("2. Penuntutan")
        print("3. Pengadilan")
        print("4. Selesai")
        
        status_map = {
            "1": "investigasi",
            "2": "penuntutan",
            "3": "pengadilan",
            "4": "selesai"
        }
        
        status = input("Pilihan (1-4): ")
        case_data["status"] = status_map[status]
        
        sanctions = input("Sanksi (optional, tekan Enter untuk kosong): ").strip()
        if sanctions:
            case_data["sanctions"] = sanctions
            
        return case_data
        
    except (ValueError, KeyError) as e:
        print(f"\nError: Input tidak valid - {str(e)}")
        return None

def main():
    """Main program loop"""
    client = CorruptionCaseClient()
    
    while True:
        print_menu()
        choice = input("Pilih menu (1-7): ")
        
        try:
            if choice == "1":
                # Lihat semua kasus
                cases = client.get_all_cases()
                print("\nDaftar Semua Kasus:")
                print(json.dumps(cases, indent=2, ensure_ascii=False))
                
            elif choice == "2":
                # Lihat detail kasus
                case_id = int(input("\nMasukkan ID kasus: "))
                case = client.get_case(case_id)
                print("\nDetail Kasus:")
                print(json.dumps(case, indent=2, ensure_ascii=False))
                
            elif choice == "3":
                # Tambah kasus baru
                case_data = get_case_input()
                if case_data:
                    created_case = client.create_case(case_data)
                    print("\nKasus berhasil ditambahkan:")
                    print(json.dumps(created_case, indent=2, ensure_ascii=False))
                
            elif choice == "4":
                # Update status kasus
                case_id = int(input("\nMasukkan ID kasus: "))
                print("\nPilih status baru:")
                print("1. Investigasi")
                print("2. Penuntutan")
                print("3. Pengadilan")
                print("4. Selesai")
                
                status_map = {
                    "1": "investigasi",
                    "2": "penuntutan",
                    "3": "pengadilan",
                    "4": "selesai"
                }
                
                status_choice = input("Pilihan (1-4): ")
                new_status = status_map[status_choice]
                timeline_desc = input("Deskripsi update: ")
                
                updated_case = client.update_case_status(case_id, new_status, timeline_desc)
                print("\nStatus kasus berhasil diupdate:")
                print(json.dumps(updated_case, indent=2, ensure_ascii=False))
                
            elif choice == "5":
                # Hapus kasus
                try:
                    case_id = int(input("\nMasukkan ID kasus yang akan dihapus: "))
                    # Get case details first
                    case_data = client.get_case(case_id)
                    confirm = input(f"Anda yakin ingin menghapus kasus '{case_data['description']}'? (Y/n): ")
                    if confirm.lower() in ['y', '']:
                        result = client.delete_case(case_id)
                        print("\nKasus berhasil dihapus")
                    elif confirm.lower() == 'n':
                        print("\nPenghapusan kasus dibatalkan")
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        print("\nError: Kasus tidak ditemukan")
                    else:
                        print(f"\nError: {str(e)}")
                except ValueError:
                    print("\nError: ID kasus harus berupa angka")
                
            elif choice == "6":
                # Lihat statistik
                stats = client.get_statistics()
                print("\nStatistik Kasus:")
                print(json.dumps(stats, indent=2, ensure_ascii=False))
                
            elif choice == "7":
                # Keluar
                print("\nTerima kasih telah menggunakan sistem ini.")
                sys.exit(0)
                
            else:
                print("\nPilihan tidak valid. Silakan pilih menu 1-7.")
                
        except requests.exceptions.RequestException as e:
            print(f"\nError: {str(e)}")
        except Exception as e:
            print(f"\nError: {str(e)}")
            
        input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()