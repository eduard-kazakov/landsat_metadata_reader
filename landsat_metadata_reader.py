class LandsatMetadataReader():

    def __init__(self, metadata_file_path):
        self.metadata_file_path = metadata_file_path
        self.metadata_file = open(self.metadata_file_path,'r')
        self.metadata = {}
        self.bands = {}

        for line in self.metadata_file.readlines():
            if (line.find('GROUP') >= 0) or (line.find('=') == -1):
                continue
            else:
                line_normalized = line.replace(' ','')
                items = line_normalized.split('=')
                self.metadata[items[0]] = items[1].replace('\n','').replace('\"','')

        if not 'SPACECRAFT_ID' in self.metadata:
            raise KeyError('Invalid metadata file')


        all_bands = []

        if self.metadata['SPACECRAFT_ID'] == 'LANDSAT_8':
            all_bands = [1,2,3,4,5,6,7,8,9,10,11]
            reflectance_bands = [1,2,3,4,5,6,7,8,9]
            thermal_bands = [10,11]

        if self.metadata['SPACECRAFT_ID'] == 'LANDSAT_7':
            all_bands = [1,2,3,4,5,'6_VCID_1','6_VCID_2',7,8]
            reflectance_bands = [1, 2, 3, 4, 5, 7, 8]
            thermal_bands = ['6_VCID_1','6_VCID_2']

        if self.metadata['SPACECRAFT_ID'] == 'LANDSAT_5':
            all_bands = [1, 2, 3, 4, 5, 6, 7]
            reflectance_bands = [1, 2, 3, 4, 5, 7]
            thermal_bands = [6]

        if self.metadata['SPACECRAFT_ID'] == 'LANDSAT_4':
            all_bands = [1, 2, 3, 4, 5, 6, 7]
            reflectance_bands = [1, 2, 3, 4, 5, 7]
            thermal_bands = [6]

        if not all_bands:
            raise KeyError('Invalid metadata file')

        for band in all_bands:
            self.bands[str(band)] = {}

            self.bands[str(band)]['file_name'] = self.metadata['FILE_NAME_BAND_%s' % band]
            self.bands[str(band)]['number'] = band
            self.bands[str(band)]['radiance_maximum'] = float(self.metadata['RADIANCE_MAXIMUM_BAND_%s' % band])
            self.bands[str(band)]['radiance_minimum'] = float(self.metadata['RADIANCE_MINIMUM_BAND_%s' % band])
            self.bands[str(band)]['quantize_cal_maximum'] = float(self.metadata['QUANTIZE_CAL_MAX_BAND_%s' % band])
            self.bands[str(band)]['quantize_cal_minumum'] = float(self.metadata['QUANTIZE_CAL_MIN_BAND_%s' % band])
            self.bands[str(band)]['radiance_mult'] = float(self.metadata['RADIANCE_MULT_BAND_%s' % band])
            self.bands[str(band)]['radiance_add'] = float(self.metadata['RADIANCE_ADD_BAND_%s' % band])

            if band in reflectance_bands:
                self.bands[str(band)]['saturation'] = self.metadata['SATURATION_BAND_%s' % band]
                self.bands[str(band)]['reflectance_maximum'] = float(self.metadata['REFLECTANCE_MAXIMUM_BAND_%s' % band])
                self.bands[str(band)]['reflectance_minimum'] = float(self.metadata['REFLECTANCE_MINIMUM_BAND_%s' % band])
                self.bands[str(band)]['reflectance_mult'] = float(self.metadata['REFLECTANCE_MULT_BAND_%s' % band])
                self.bands[str(band)]['reflectance_add'] = float(self.metadata['REFLECTANCE_ADD_BAND_%s' % band])

            if band in thermal_bands:
                self.bands[str(band)]['k1_constant'] = float(self.metadata['K1_CONSTANT_BAND_%s' % band])
                self.bands[str(band)]['k2_constant'] = float(self.metadata['K2_CONSTANT_BAND_%s' % band])

    def get_band_metadata_by_file_name(self, file_name):
        for band in self.bands.keys():
            if file_name == self.bands[band]['file_name']:
                return self.bands[band]

#metadata = LandsatMetadataReader('samples/LC08_L1TP_179018_20190606_20190619_01_T1/LC08_L1TP_179018_20190606_20190619_01_T1_MTL.txt')
#print metadata.get_band_metadata_by_file_name('LC08_L1TP_179018_20190606_20190619_01_T1_B11.TIF')