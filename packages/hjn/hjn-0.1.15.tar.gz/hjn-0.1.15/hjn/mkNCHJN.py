#coding=utf8
import numpy as np
import netCDF4 as nc
import datetime
import traceback

class ttt():
	def __init__(self,a):
		print(a)

class envelope():
	def __init__(self,n,s,w,e):
		self.n,self.s,self.w,self.e=n,s,w,e
        
LeftTopCornerPairArr = np.asarray([
#   //东北
    {"area":"NEC", "evn":envelope(55, 38,109, 136)},
#   //华北
    {"area":"NCN", "evn":envelope(43,31, 109,124)},
#     //华中
    {"area":"CCN", "evn":envelope(36,22, 108, 124)},
#     //华南
    {"area":"SCN", "evn":envelope(27, 15,104, 124)},
#     //西北
    {"area":"NWC", "evn":envelope(44,31, 88, 114)},
#     //西南
    {"area":"SWC", "evn":envelope(35, 20,96, 111)},
#     //新疆
    {"area":"XJ", "evn":envelope(50, 34,72, 97)},
#     //西藏
    {"area":"XZ", "evn":envelope(37,25, 77, 101)}])

class dataClass():
	data_ = None
	name_ = None
	type_ = np.float32
	coordinate_ = None
	unit_ = None
	valid_range_ = [-999,999]
	missing_value_ = np.NAN
	scala_factor_ = np.float32(1.0)
	add_offset_ = np.float32(0.0)

	def __init__(self,data, name, type_,coordinate, unit,missing_value=np.NAN, scala_factor=np.float32(1.0), add_offset=np.float32(0.0),valid_range=[-999,999]):
		self.data_, self.name_, self.type_, self.coordinate_, self.unit_ ,self.missing_value_ ,self.scala_factor_,self.add_offset_,self.valid_range_= data, name,type_, coordinate, unit,missing_value, scala_factor, add_offset, valid_range

	def print(self):
		print(self.data_, self.name_, self.type_, self.coordinate_, self.unit_,self.missing_value_,self.scala_factor_,self.add_offset_,self.valid_range_)
		
def mkNCCommonUni(output,dateTimeStart,dateTimeArr,isoArr,latArr,lonArr,dataClass4D=[],dataClass3D=[],dataClass2D=[]):
    dataset = nc.Dataset(output,'w',format='NETCDF4') #'NETCDF4_CLASSIC')
    
    try:
    
        dataset.createDimension("time", len(dateTimeArr))
        if not isoArr is None:
            dataset.createDimension("isobaric", len(isoArr))
        
        dataset.createDimension("lat", len(latArr))
        dataset.createDimension("lon", len(lonArr))
    
    
        dataset.createVariable("time", np.float32, ("time"), zlib=True)
        if not isoArr is None:
            dataset.createVariable("isobaric", np.float32, ("isobaric"), zlib=True)
        dataset.createVariable("lat", np.float32, ("lat"), zlib=True)
        dataset.createVariable("lon", np.float32, ("lon"), zlib=True)

        for e in dataClass2D:
            dataset.createVariable(e.name_, e.type_, tuple(["lat","lon"]), zlib=True)    

        for e in dataClass3D:
            dataset.createVariable(e.name_, e.type_, tuple(["time","lat","lon"]), zlib=True)

        for e in dataClass4D:
            dataset.createVariable(e.name_, e.type_, tuple(["time","isobaric","lat","lon"]), zlib=True)
    
        dataset.variables["time"][:] = dateTimeArr
        dataset.variables["time"].units = 'minutes since %s'%(dateTimeStart.strftime("%Y-%m-%d %H:%M:%S"))
        dataset.variables["time"].calendar = 'gregorian'

        if not isoArr is None:
            dataset.variables["isobaric"][:] = isoArr
            dataset.variables["isobaric"].units="hPa"
            dataset.variables["isobaric"].positive="up"
        
        dataset.variables["lat"][:] = latArr
        dataset.variables['lat'].units = 'degrees_north'
    
        dataset.variables["lon"][:] = lonArr
        dataset.variables['lon'].units = 'degrees_east'
        
        for e in dataClass2D:
            dataset.variables[e.name_][:] = e.data_
            dataset.variables[e.name_].units = e.unit_
            dataset.variables[e.name_].valid_range = e.valid_range_
            dataset.variables[e.name_].coordinate = e.coordinate_
            dataset.variables[e.name_].missing_value = e.missing_value_
            dataset.variables[e.name_].scala_factor = e.scala_factor_
            dataset.variables[e.name_].add_offset = e.add_offset_
    
        for e in dataClass3D:
            dataset.variables[e.name_][:] = e.data_
            dataset.variables[e.name_].units = e.unit_
            dataset.variables[e.name_].valid_range = e.valid_range_
            dataset.variables[e.name_].coordinate = e.coordinate_
            dataset.variables[e.name_].missing_value = e.missing_value_
            dataset.variables[e.name_].scala_factor = e.scala_factor_
            dataset.variables[e.name_].add_offset = e.add_offset_

        for e in dataClass4D:
            dataset.variables[e.name_][:] = e.data_
            dataset.variables[e.name_].units = e.unit_
            dataset.variables[e.name_].valid_range = e.valid_range_
            dataset.variables[e.name_].coordinate = e.coordinate_
            dataset.variables[e.name_].missing_value = e.missing_value_
            dataset.variables[e.name_].scala_factor = e.scala_factor_
            dataset.variables[e.name_].add_offset = e.add_offset_

        #dataset.close()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        #dataset.close()
    finally:
        dataset.close()

def clip(data, ltc, lat0, lon0, step):
    latIdx0 = int((lat0 - ltc.n) / step+ 0.5)
    latIdx1 = int((lat0 - ltc.s) / step+ 0.5)
    lonIdx0 = int((ltc.w - lon0) / step+ 0.5)
    lonIdx1 = int((ltc.e - lon0) / step+ 0.5)
    data = data[latIdx0:latIdx1+1, lonIdx0:lonIdx1+1]
    return data


