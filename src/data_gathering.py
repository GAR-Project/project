import influxdb, sys

QUERY = """SELECT DERIVATIVE(icmp_inechos) AS d_ping FROM net ORDER BY time DESC LIMIT 100"""

n_samples, mean = 0, 0

if __name__ == "__main__":
    if len(sys.argv) == 2:
        db = influxdb.InfluxDBClient('10.0.123.3', 8086, 'root', 'root', 'h4_net_stats')
        measurement_class = sys.argv[1]
    elif len(sys.argv) == 3:
        db = influxdb.InfluxDBClient(sys.argv[1], 8086, 'root', 'root', 'h4_net_stats')
        measurement_class = sys.argv[1]
    elif len(sys.argv) == 4:
        db = influxdb.InfluxDBClient(sys.argv[1], int(sys.argv[2]), 'root', 'root', 'h4_net_stats')
        measurement_class = sys.argv[1]
    elif len(sys.argv) == 5:
        db = influxdb.InfluxDBClient(sys.argv[1], int(sys.argv[2]), 'root', 'root', sys.argv[3])
        measurement_class = sys.argv[1]
    else:
        print("Usage: python3 " + sys.argv[0] + " 0 | 1 [InfluxDB_IP] [InfluxDB_port] [DB_name]")
        exit(-1)

    out_file = open("ICMP_data_class_{}.csv".format(measurement_class), "w+")

    for measurement in db.query(QUERY).get_points(measurement = 'net'):
        curr_derivative = measurement["d_ping"]
        n_samples += 1
        delta_mean = (curr_derivative - mean) / n_samples
        mean += delta_mean
        out_file.write("{}, {}, {}\n".format(curr_derivative, mean, measurement_class))

    out_file.close()
    print("Finished!")
    exit(0)