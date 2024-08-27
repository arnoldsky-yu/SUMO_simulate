import xml.etree.ElementTree as ET

tree = ET.parse('tripinfo.xml')
root = tree.getroot()

time_loss_values = []

for trip in root.findall('tripinfo'):
    time_loss = float(trip.get('timeLoss'))
    time_loss_values.append(time_loss)

average_time_loss = sum(time_loss_values) / len(time_loss_values)

print(f"Average timeLoss: {average_time_loss:.2f} seconds")
