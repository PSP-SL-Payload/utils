#!/usr/bin/env python
import matplotlib.pyplot as plt


def GetTimeSec(line):
    timeString = line.split(',')[0]
    millis  = int(timeString.split('.')[1])
    seconds = int(timeString.split(':')[2].split('.')[0])
    minutes = int(timeString.split(':')[1])
    hours   = int(timeString.split(':')[0])

    return millis/1000 + seconds + minutes*60 + hours*3600


if __name__ == "__main__":
    with open('flightData.txt') as logs:
        lines = logs.readlines()

        lines.remove(lines[0]) # Remove the first line (header)

        times = [GetTimeSec(line) for line in lines]
        stage = [int(line.split(',')[1]) for line in lines]
        altitude_m = [float(line.split(',')[2]) for line in lines]
        accel_x = [float(line.split(',')[3]) for line in lines]
        accel_y = [float(line.split(',')[4]) for line in lines]
        accel_z = [float(line.split(',')[5]) for line in lines]
        accel_net = [pow(pow(accel_x[i], 2) + pow(accel_y[i], 2) + pow(accel_z[i], 2), 0.5) for i in range(len(accel_x))]


        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        # Altitude vs Time
        ax1.set_title('Altitude vs Time')
        ax1.plot(times, altitude_m)
        ax1.grid(True)
        ax1.set(ylabel='Altitude (m)')
        
        # Stage vs Time
        ax2.set_title('Stage vs Time')
        ax2.plot(times, stage)
        ax2.grid(True)
        ax2.set(xlabel='Time (s)', ylabel='Stage')

        # Acceleration_net vs Time
        ax3.set_title('Acceleration_net vs Time')
        ax3.plot(times, accel_net)
        ax3.grid(True)
        ax3.set(xlabel='Time (s)', ylabel='Acceleration_net (m/s^2)')


        plt.show()
    


