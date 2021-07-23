import psutil
import os
import json

class File:
    def __init__(self) -> None:
        self.__init_comp = False
        self.__cache_path = ".\cache"
        self.__init_checks()

    def __init_checks(self):
        """A simple method to check and create necessary directories on launch"""
        if os.path.isdir(self.__cache_path):
            self.__init_comp = True
        else:
            try:
                os.mkdir(self.__cache_path)
                self.__init_comp = True
            except Exception as e:
                print("\n\n\nThe following exception was thrown from the File class\n\n"+e)
    
    def get_cache_path(self) -> str:
        """Returns the path of the cache folder"""
        return self.__cache_path
    
    def __write_to_cache(self, filename:str , data) -> bool:
        """Method to write data to cache easily. give only filename no extension."""
        path = os.path.join(self.__cache_path,filename+".json")
        print("writing to cache:\t"+path)
        # if os.path.isfile(path):
        try:
            with open(path, "w", encoding="UTF-8") as f:
                if type(data) == str:
                    f.writelines(data)
                    f.close()
                    print("wrote string")
                else:
                    f.writelines(json.dumps(data))
                    f.close()
                    print("wrote dictionary")
            return True
        except Exception as e:
            print("\n\nException occured while writing to cache:\n"+e)
            return False
        # else:
        #     return False
    
    def __read_from_cache(self, filename:str) -> dict:
        """Method to write data to cache easily. give only filename no extension."""
        path = self.__cache_path+filename+".json"
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="UTF-8") as f:
                    data = json.loads(f.readlines())
                    f.close()
                return data
            except Exception as e:
                print("\n\nException occured while Reading from cache:\n"+e)
                return False
        else:
            return False


class settings(File):
    def __init__(self) -> None:
        super(settings, self).__init__()
        self.__settings = dict()
        self.__def_settings = {
            "scrape_interval" : 5,
            "cpu" : True,
            "RAM" : True,
            "Disk" : True,
            "Net" : True,
            "port" : 9191,
            "enabled" : True,
            "cache_path" : ".\cache",
            # "setting_name" : "settings",
            "data_name" : "data"
        }
        self.__set_path = self._File__cache_path+"\settings.json"
        self.__init_settings()

    def __init_settings(self):
        if os.path.isfile(self.__set_path):
            try:
                temp = self._File__read_from_cache("settings")
                if temp == False:
                    self.__settings = self.__def_settings
                    self._File__write_to_cache("settings", self.__settings)
                else:
                    self.__settings = temp
            except Exception as e:
                print("\n\nerror initializing settings:\n\n"+e)
        else:
            self.__settings = self.__def_settings
            self._File__write_to_cache("settings", self.__settings)


    def save_settings(self) -> bool:
        """Saves the current setting configuration"""
        return self._File__write_to_cache("settings", self.__settings)
    
    def change_setting(self, setting:dict) -> bool:
        """a method to change the current setting configuration"""
        self.__settings = setting
        return self.save_settings()

    def get_settings(self) -> dict:
        """returns the current settings configuration"""
        return self.__settings

class scraper(File):
    def __init__(self) -> None:
        super(scraper, self).__init__()
        self.__enabled = False
        self.__data_path = str()
        self.__cached_data = dict()
        self.__cd_def = {
            "RAM":[],
            "cpu":[],
            "net":[],
            "disk":[]
        }
        self.__settings_copy = dict()

    def __get_cached_data(self):
        pass

    # def set_path(self,setting: str) -> bool:
    #     """Sets the path for data to be sent to. Set this using the settings class"""
    #     try:
    #         self.__data_path = setting
    #         self.__enabled = True
    #         return True
    #     except Exception as e:
    #         print("\n\nerror setting the data path\n"+e)
    #         return False
    
    def return_cache(self) -> dict:
        """returns the cache dictionary"""
        return self.__cached_data

    def set_copy(self,copy):
        self.__settings_copy = copy

    def scrape_data(self):
        print(self.__cached_data)
        if not self.__cached_data:
            self.__cached_data = self.__cd_def
        if self.__settings_copy['cpu']:
            self.__cached_data['cpu'].append(psutil.cpu_percent())
        if self.__settings_copy['RAM']:
            self.__cached_data['RAM'].append(psutil.virtual_memory().percent)
        if self.__settings_copy['Disk']:
            self.__cached_data['disk'].append(psutil.disk_usage('C:\\').percent)
        # if self.__settings_copy['Net']:
        #     self.__cached_data['net'].append(psutil.net_if_stats())  /* Research more into this field */
        self.__save_cache()

    def __save_cache(self):
        self._File__write_to_cache("data",self.__cached_data)