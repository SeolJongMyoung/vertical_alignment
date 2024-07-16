# main.py

from vertical_alignment import VerticalAlignment

def main():
    # 입력 데이터
    start_station = 0
    start_elevation = 67.4995
    ips = [
        (105.0549, 68.6857, 80),  # (station, elevation, curve_length)
        (219.3407, 59.6905, 60),
        (331.2134, 60.4200, 60)
    ]
    end_station = 460.0
    end_elevation = 60.6244

    # VerticalAlignment 객체 생성
    va = VerticalAlignment(start_station, start_elevation, ips, end_station, end_elevation)

    # 결과 출력
    print(f"시작점: station {start_station}m, 고도 {start_elevation:.2f}m")
    for i, ip in enumerate(ips, 1):
        print(f"IP{i}: station {ip[0]}m, 고도 {ip[1]:.2f}m, 곡선 길이 {ip[2]}m")
    print(f"종점: station {end_station}m, 고도 {end_elevation:.2f}m")

    grades = va.calculate_grades()
    for i, grade in enumerate(grades, 1):
        print(f"경사도 {i}: {grade:.2f}%")

    # DXF 파일 생성
    va.create_dxf('vertical_alignment_multi_ip.dxf')
    print("DXF 파일이 생성되었습니다: vertical_alignment_multi_ip.dxf")

    # 20m 간격으로 고도 출력
    stations, elevations = va.generate_profile()
    print("\n20m 간격 고도 출력 (1m 간격으로 계산):")
    for i in range(0, len(stations), 20):
        print(f"지점: {stations[i]}m, 고도: {elevations[i]:.2f}m")

if __name__ == "__main__":
    main()