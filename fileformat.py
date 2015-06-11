from struct import pack,unpack
from copy import deepcopy,copy

import re

class FormatControl:
    ext = None
    filename = None
    file_information = []
    buf = ""
    file_length = 0
    
    def __init__(self,ext,filename):
        self.ext = ext
        self.filename = filename

    def find_all(self,data,string):
        string_index = []
        for m in re.finditer(string,data):
            string_index.append({
                "startOffset" : m.start(),
                "endOffset" : m.end()
            })

        return string_index
        
    def aviFormat(self):
        format_data = []

        if self.ext != "avi":
            print "[+] file format is + baseOffset not avi"
            return -1
    
        fp = open(self.filename,"rb")
        self.buf = fp.read()

        self.file_length = len(self.buf)
        RIFF = self.find_all(self.buf,"RIFF")
        LIST = self.find_all(self.buf,"LIST")


        format_data.append({
            "RIFF" : {
                "data" : self.buf[RIFF[0]["startOffset"]:RIFF[0]["endOffset"]],
                "startOffset" : RIFF[0]["startOffset"],
                "endOffset" : RIFF[0]["endOffset"],
            },

            "RIFFSize" : {
                "data" : unpack('<L', self.buf[RIFF[0]["startOffset"]+4:RIFF[0]["endOffset"]+4])[0],
                "startOffset" : RIFF[0]["startOffset"]+4,
                "endOffset" : RIFF[0]["endOffset"]+4,
            },


            "RIFFType" : {
                "data" : unpack('<L', self.buf[RIFF[0]["startOffset"]+8:RIFF[0]["endOffset"]+8])[0],
                "startOffset" : RIFF[0]["startOffset"]+8,
                "endOffset" : RIFF[0]["endOffset"]+8,
            },
        })


        for attr in LIST:
            format_data.append({
                "LIST" : {
                    "data" : self.buf[attr["startOffset"]:attr["endOffset"]],
                    "startOffset" : attr["startOffset"],
                    "endOffset" : attr["endOffset"],
                },

                "LISTSize" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0],
                    "startOffset" : attr["startOffset"]+4,
                    "endOffset" : attr["endOffset"] +4,
                },

                "LISTType" : {
                    "data" : self.buf[attr["startOffset"]+8:attr["endOffset"]+8],
                    "startOffset" : attr["startOffset"]+8,
                    "endOffset" : attr["endOffset"] + 8,
                }
            })

        avih = self.find_all(self.buf,"avih")[0]

        format_data.append({
            "avih" : {
                "data" : self.buf[avih["startOffset"]:avih["endOffset"]],
                "startOffset" : avih["startOffset"],
                "endOffset" : avih["endOffset"],
            },

            "avihSize" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+4:avih["endOffset"]+4])[0],
                "startOffset" : avih["startOffset"]+4,
                "endOffset" : avih["endOffset"]+4,
            },


            "avihMicroSecPerFrame" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+8:avih["endOffset"]+8])[0],
                "startOffset" : avih["startOffset"]+8,
                "endOffset" : avih["endOffset"]+8
            },

            "avihMaxBytesPerSec" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+12:avih["endOffset"]+12])[0],
                "startOffset" : avih["startOffset"]+12,
                "endOffset" : avih["endOffset"]+12
            },

            "avihPaddingGranularity" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+16:avih["endOffset"]+16])[0],
                "startOffset" : avih["startOffset"]+16,
                "endOffset" : avih["endOffset"]+16
            },

            "avihFlags" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+20:avih["endOffset"]+20])[0],
                "startOffset" : avih["startOffset"]+20,
                "endOffset" : avih["endOffset"]+20
            },

            "avihTotalFrames" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+24:avih["endOffset"]+24])[0],
                "startOffset" : avih["startOffset"]+24,
                "endOffset" : avih["endOffset"]+24
            },

            "avihInitialFrames" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+28:avih["endOffset"]+28])[0],
                "startOffset" : avih["startOffset"]+28,
                "endOffset" : avih["endOffset"]+28
            },

            "avihStream" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+32:avih["endOffset"]+32])[0],
                "startOffset" : avih["startOffset"]+32,
                "endOffset" : avih["endOffset"]+32,
            },

            "avihStream" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+32:avih["endOffset"]+32])[0],
                "startOffset" : avih["startOffset"]+32,
                "endOffset" : avih["endOffset"]+32
            },

            "avihSuggestedBufferSize" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+36:avih["endOffset"]+36])[0],
                "startOffset" : avih["startOffset"]+36,
                "endOffset" : avih["endOffset"]+36
            },

            "avihWidth" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+40:avih["endOffset"]+40])[0],
                "startOffset" : avih["startOffset"]+40,
                "endOffset" : avih["endOffset"]+40
            },

            "avihHeight" : {
                "data" :  unpack('<L', self.buf[avih["startOffset"]+44:avih["endOffset"]+44])[0],
                "startOffset" : avih["startOffset"]+44,
                "endOffset" : avih["endOffset"]+44
            }
        })


        strh = self.find_all(self.buf,"strh")

        for attr in strh:
            format_data.append({
                "strhID" : {
                    "data" : self.buf[attr["startOffset"]:attr["endOffset"]],
                    "startOffset" : attr["startOffset"],
                    "endOffset" : attr["endOffset"],
                },

                "strhSize" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0],
                    "startOffset" : attr["startOffset"]+4,
                    "endOffset" : attr["endOffset"]+4,
                },

                "strhType1" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+8:attr["endOffset"]+8])[0],
                    "startOffset" : attr["startOffset"]+8,
                    "endOffset" : attr["endOffset"]+8,
                },

                "strhType2" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+12:attr["endOffset"]+12])[0],
                    "startOffset" : attr["startOffset"]+12,
                    "endOffset" : attr["endOffset"]+12,
                },

                "strhFlags" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+16:attr["endOffset"]+16])[0],
                    "startOffset" : attr["startOffset"]+16,
                    "endOffset" : attr["endOffset"]+16,
                },

                "strhPriority" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+20:attr["endOffset"]+20])[0],
                    "startOffset" : attr["startOffset"]+20,
                    "endOffset" : attr["endOffset"]+20,
                },

                "strhLanguage" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+24:attr["endOffset"]+24])[0],
                    "startOffset" : attr["startOffset"]+24,
                    "endOffset" : attr["endOffset"]+24,
                },

                "strhScale" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+28:attr["endOffset"]+28])[0],
                    "startOffset" : attr["startOffset"]+28,
                    "endOffset" : attr["endOffset"]+28,
                },

                "strhRate" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+32:attr["endOffset"]+32])[0],
                    "startOffset" : attr["startOffset"]+32,
                    "endOffset" : attr["endOffset"]+32,
                },

                "strhStart" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+36:attr["endOffset"]+36])[0],
                    "startOffset" : attr["startOffset"]+36,
                    "endOffset" : attr["endOffset"]+36,
                },

                "strhLength" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+40:attr["endOffset"]+40])[0],
                    "startOffset" : attr["startOffset"]+40,
                    "endOffset" : attr["endOffset"]+40,
                },

                "strhSuggestedBufferSize" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+44:attr["endOffset"]+44])[0],
                    "startOffset" : attr["startOffset"]+44,
                    "endOffset" : attr["endOffset"]+44,
                },

                "strhQuality" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+48:attr["endOffset"]+48])[0],
                    "startOffset" : attr["startOffset"]+48,
                    "endOffset" : attr["endOffset"]+48,
                },

                "strhSampleSize" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+52:attr["endOffset"]+52])[0],
                    "startOffset" : attr["startOffset"]+52,
                    "endOffset" : attr["endOffset"]+52,
                },
            })

        strf = self.find_all(self.buf,"strf")

        for attr in strf:
            if unpack('<L',self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0] == 40:
                # video stream
                format_data.append({
                    "strfID" : {
                        "data" : self.buf[attr["startOffset"]:attr["endOffset"]],
                        "startOffset" : attr["startOffset"],
                        "endOffset" : attr["endOffset"],
                    },

                    "strfSize" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0],
                        "startOffset" : attr["startOffset"]+4,
                        "endOffset" : attr["endOffset"]+4,
                    },

                    "strfbiSize" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+8:attr["endOffset"]+8])[0],
                        "startOffset" : attr["startOffset"]+8,
                        "endOffset" : attr["endOffset"]+8,
                    },

                    "strfbiWidth" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+12:attr["endOffset"]+12])[0],
                        "startOffset" : attr["startOffset"]+12,
                        "endOffset" : attr["endOffset"]+12,
                    },

                    "strfbiHeight" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+16:attr["endOffset"]+16])[0],
                        "startOffset" : attr["startOffset"]+16,
                        "endOffset" : attr["endOffset"]+16,
                    },

                    "strfbiPlanes" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+20:attr["endOffset"]+20])[0],
                        "startOffset" : attr["startOffset"]+20,
                        "endOffset" : attr["endOffset"]+20,
                    },

                    "strfbiBitCount" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+24:attr["endOffset"]+24])[0],
                        "startOffset" : attr["startOffset"]+24,
                        "endOffset" : attr["endOffset"]+24,
                    },

                    "strfbiCompression" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+28:attr["endOffset"]+28])[0],
                        "startOffset" : attr["startOffset"]+28,
                        "endOffset" : attr["endOffset"]+28,
                    },

                    "strfbiSizeImage" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+32:attr["endOffset"]+32])[0],
                        "startOffset" : attr["startOffset"]+32,
                        "endOffset" : attr["endOffset"]+32,
                    },

                    "strfbiXPelsPerMeter" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+36:attr["endOffset"]+36])[0],
                        "startOffset" : attr["startOffset"]+36,
                        "endOffset" : attr["endOffset"]+36,
                    },

                    "strfbiYPelsPerMeter" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+40:attr["endOffset"]+40])[0],
                        "startOffset" : attr["startOffset"]+40,
                        "endOffset" : attr["endOffset"]+40,
                    },

                    "strfClrUsed" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+44:attr["endOffset"]+44])[0],
                        "startOffset" : attr["startOffset"]+44,
                        "endOffset" : attr["endOffset"]+44,
                    },

                    "strfClrImportant" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+48:attr["endOffset"]+48])[0],
                        "startOffset" : attr["startOffset"]+48,
                        "endOffset" : attr["endOffset"]+48,
                    },
                })

            else:
                format_data.append({
                    "strfID" : {
                        "data" : self.buf[attr["startOffset"]:attr["endOffset"]],
                        "startOffset" : attr["startOffset"],
                        "endOffset" : attr["endOffset"],
                    },

                    "strfSize" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0],
                        "startOffset" : attr["startOffset"]+4,
                        "endOffset" : attr["endOffset"]+4,
                    },

                    "strfwFormatTag" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+8:attr["endOffset"]+8])[0],
                        "startOffset" : attr["startOffset"]+8,
                        "endOffset" : attr["endOffset"]+8,
                    },

                    "strfnChannels" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+12:attr["endOffset"]+12])[0],
                        "startOffset" : attr["startOffset"]+12,
                        "endOffset" : attr["endOffset"]+12,
                    },

                    "strfnSamplesPerSec" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+16:attr["endOffset"]+16])[0],
                        "startOffset" : attr["startOffset"]+16,
                        "endOffset" : attr["endOffset"]+16,
                    },

                    "strfnAvgBytesPerSec" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+20:attr["endOffset"]+20])[0],
                        "startOffset" : attr["startOffset"]+20,
                        "endOffset" : attr["endOffset"]+20,
                    },

                    "strfnBlockAlign" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+24:attr["endOffset"]+24])[0],
                        "startOffset" : attr["startOffset"]+24,
                        "endOffset" : attr["endOffset"]+24,
                    },

                    "strfwBitsPerSample" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+28:attr["endOffset"]+28])[0],
                        "startOffset" : attr["startOffset"]+28,
                        "endOffset" : attr["endOffset"]+28,
                    },

                    "strfcbSize" : {
                        "data" : unpack('<L', self.buf[attr["startOffset"]+32:attr["endOffset"]+32])[0],
                        "startOffset" : attr["startOffset"]+32,
                        "endOffset" : attr["endOffset"]+32,
                    },

                })


        idx1 = self.find_all(self.buf,"idx1")

        for attr in idx1:
            format_data.append({
                "idx1" : {
                    "data" : self.buf[attr["startOffset"]:attr["endOffset"]],
                    "startOffset" : attr["startOffset"],
                    "endOffset" : attr["endOffset"],
                },

                "idx1Size" : {
                    "data" : unpack('<L', self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0],
                    "startOffset" : attr["startOffset"]+4,
                    "endOffset" : attr["endOffset"]+4,
                },

                "mov1data" : {
                    "data" : self.buf[attr["startOffset"]+8:attr["startOffset"]+8+unpack('<L', self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0]],
                    "startOffset" : attr["startOffset"]+8,
                    "endOffset" : attr["startOffset"]+8 + unpack('<L', self.buf[attr["startOffset"]+4:attr["endOffset"]+4])[0],
                }
            })

        fp.close()
        return format_data

