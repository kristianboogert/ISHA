import pandas as pd
import xlsxwriter

# export bodypart angles to an excel sheet
def export_to_line_chart(filename, data, sheet_name="Sheet1"):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    headings = ['xy', 'xz', 'yz']
    if len(data) != 3:
        print("Data is not in the correct format. Please provide [xy], [yz] and [xz] angles")
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])
    chart1 = workbook.add_chart({'type': 'line'}) 
    chart1.add_series({'values': '=Sheet1!$A$1:$A$'+str(len(data[0])), 'name': 'xy angles', 'line': {'color': 'red'}})
    chart1.add_series({'values': '=Sheet1!$B$1:$B$'+str(len(data[1])), 'name': 'xz angles', 'line': {'color': 'green'}})
    chart1.add_series({'values': '=Sheet1!$C$1:$C$'+str(len(data[2])), 'name': 'yz angles', 'line': {'color': 'blue'}})
    chart1.set_title ({'name': 'Pose data'}) 
    chart1.set_x_axis({'name': 'Camera frame'})
    chart1.set_y_axis({'name': 'Angle'})
    chart1.set_style(11)
    worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
    workbook.close()