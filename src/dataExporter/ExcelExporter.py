import pandas as pd
import xlsxwriter

# export bodypart angles to an excel sheet
def export_to_line_chart(filename, data, exercise_name=None, sheet_name="Sheet1"):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    headings = ['xy', 'xz', 'yz', 'elapsed milliseconds since exercise start']
    if len(data) != 4:
        print("Data is not in the correct format. Please provide [xy], [yz] and [xz] angles as well as [time]")
    # fix time in data
    start_ms = data[3][0]
    for pos in range(len(data[3])):
        data[3][pos] -= start_ms
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])
    worksheet.write_column('D2', data[3])
    chart1 = workbook.add_chart({'type': 'line'})
    chart1.add_series({
        'categories': '=Sheet1!$D$1:$D$'+str(len(data[3])), 'name': 'elapsed milliseconds since exercise start',
        'values': '=Sheet1!$A$1:$A$'+str(len(data[0])), 'name': ' xy plane angles in degrees', 'line': {'color': 'red'}
    })
    chart1.add_series({
        'categories': '=Sheet1!$D$1:$D$'+str(len(data[3])), 'name': 'elapsed milliseconds since exercise start',
        'values': '=Sheet1!$B$1:$B$'+str(len(data[1])), 'name': 'xz plane angles in degrees', 'line': {'color': 'green'}
    })
    chart1.add_series({
        'categories': '=Sheet1!$D$1:$D$'+str(len(data[3])), 'name': 'elapsed milliseconds since exercise start',
        'values': '=Sheet1!$C$1:$C$'+str(len(data[2])), 'name': 'yz plane angles in degrees', 'line': {'color': 'blue'}
    })
    graph_title = 'Pose data'
    if exercise_name is not None:
        graph_title+=(": "+exercise_name)
    chart1.set_title ({'name': graph_title})
    chart1.set_x_axis({'name': 'Elapsed milliseconds since exercise start'})
    chart1.set_y_axis({'name': 'Angle'})
    chart1.set_style(11)
    worksheet.insert_chart('E2', chart1, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
