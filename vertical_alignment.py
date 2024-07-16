# vertical_alignment.py

import math
import ezdxf

class VerticalAlignment:
    def __init__(self, start_station, start_elevation, ips, end_station, end_elevation):
        self.start_station = start_station
        self.start_elevation = start_elevation
        self.ips = ips
        self.end_station = end_station
        self.end_elevation = end_elevation

    def calculate_elevation(self, x):
        if x <= self.start_station:
            return self.start_elevation
        if x >= self.end_station:
            return self.end_elevation

        for i, current_ip in enumerate(self.ips):
            ip_station, ip_elevation, curve_length = current_ip
            
            if i == 0:
                prev_station, prev_elevation = self.start_station, self.start_elevation
            else:
                prev_ip = self.ips[i-1]
                prev_station, prev_elevation = prev_ip[0], prev_ip[1]
            
            if i == len(self.ips) - 1:
                next_station, next_elevation = self.end_station, self.end_elevation
            else:
                next_ip = self.ips[i+1]
                next_station, next_elevation = next_ip[0], next_ip[1]
            
            bvc_station = ip_station - curve_length / 2
            evc_station = ip_station + curve_length / 2
            
            if x < bvc_station:
                grade = (ip_elevation - prev_elevation) / (ip_station - prev_station)
                return prev_elevation + grade * (x - prev_station)
            elif bvc_station <= x <= evc_station:
                grade1 = (ip_elevation - prev_elevation) / (ip_station - prev_station)
                grade2 = (next_elevation - ip_elevation) / (next_station - ip_station)
                R = curve_length / (grade2 - grade1)
                x1 = x - bvc_station
                y_offset = R * (1 - math.cos(x1 / R))
                return prev_elevation + grade1 * (bvc_station - prev_station) + grade1 * x1 + y_offset
            elif x > evc_station:
                if i == len(self.ips) - 1 or x < self.ips[i+1][0] - self.ips[i+1][2]/2:
                    grade = (next_elevation - ip_elevation) / (next_station - ip_station)
                    return ip_elevation + grade * (x - ip_station)
                else:
                    continue

        raise ValueError(f"Station {x}m에 대한 고도를 계산할 수 없습니다.")

    def calculate_grades(self):
        grades = []
        for i in range(len(self.ips) + 1):
            if i == 0:
                start = self.start_station, self.start_elevation
                end = self.ips[0][0], self.ips[0][1]
            elif i == len(self.ips):
                start = self.ips[-1][0], self.ips[-1][1]
                end = self.end_station, self.end_elevation
            else:
                start = self.ips[i-1][0], self.ips[i-1][1]
                end = self.ips[i][0], self.ips[i][1]
            
            grade = (end[1] - start[1]) / (end[0] - start[0]) * 100
            grades.append(grade)
        return grades

    def generate_profile(self):
        stations = list(range(int(self.start_station), int(self.end_station) + 1))
        elevations = [self.calculate_elevation(x) for x in stations]
        return stations, elevations

    def create_dxf(self, filename):
        stations, elevations = self.generate_profile()

        doc = ezdxf.new('R2010')
        msp = doc.modelspace()

        points = list(zip(stations, elevations))
        msp.add_lwpolyline(points)

        key_points = [(self.start_station, self.start_elevation, '시작점')] + \
                     [(ip[0], ip[1], f'IP{i+1}') for i, ip in enumerate(self.ips)] + \
                     [(self.end_station, self.end_elevation, '종점')]

        for station, elevation, label in key_points:
            msp.add_circle((station, elevation), radius=1)
            
            # 텍스트 생성 및 위치 설정
            text = msp.add_text(label)
            text.dxf.height = 2
            text.dxf.align_point = (station, elevation + 2)
            text.dxf.halign = ezdxf.lldxf.const.CENTER
            text.dxf.valign = ezdxf.lldxf.const.BOTTOM

        doc.saveas(filename)    