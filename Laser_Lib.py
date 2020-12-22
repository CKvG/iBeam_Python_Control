# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:43:05 2020

@author: grundch
"""


import serial
import time

# Some variables for Testing, delete when finalised
terminalString_getTemp = "%SYS-I-077, scaled\r\nTEMP = 025.0  C  \r\nCMD>"
terminalString_getPower = "%SYS-I-077, scaled\r\nPIC  = 000000 uW  \r\nCMD>"

class iBeam():

    def __init__(self): # @todo CS
        self.ser = serial.Serial() # @todo CS
        self.ser.baudrate = 115200
        self.ser.timeout = 0.5

    # =============================================================================
    #   Connection
    # =============================================================================
    def connect(self, port):
        """ Connect to COM-Port/iBeam

            Parameters
            ----------
            port : string
                The Port iBeam is connected to - i.e. "COMX"
            Returns
            -------

        """
        self.ser.port = port
        self.ser.open()
        if (self.ser.is_open == True):
            print('connected')
        else:
            print('ERROR: connection error')
        return self.ser

    def disconnect(self):
        """ Disconnect from COM-Port/iBeam

            Parameters
            ----------

            Returns
            -------

        """
        self.ser.close()
        if (self.ser.is_open == False):
            print('disconnected')
        else:
            print('ERROR: connection error')

    # =============================================================================
    #   General Laser and Channel Control
    # =============================================================================

    def setLaserPowerIn_uW(self, channel, powerIn_uW):
        """ Set power in micro watts for specified channel

            Parameters
            ----------
            channel : int
                Channel number [1..2]
            powerIn_uW : float
                Power in micro watts
            Returns
            -------
        """
        channel_str = bytes(channel)
        powerIn_uW_str = bytes([powerIn_uW])
        self.ser.write(b'ch ' + channel_str + b' power ' + powerIn_uW_str + b'mic\r\n')

    def setLaserPowerIn_mW(self, channel, powerIn_mW):
        """ Set power in milli watts for specified channel

            Parameters
            ----------
            channel : int
                Channel number [1..2]
            powerIn_mW : float
                Power in milli watts

            Returns
            -------
        """
        channel_str = bytes(channel, encoding="utf-8")
        powerIn_mW_b = bytes(powerIn_mW, encoding="utf-8")
        self.ser.write(b'ch ' + channel_str + b' power ' + powerIn_mW_b + b'\r\n')

    def setLaserON(self):
        """ activate LD driver

            Parameters
            ----------
            Returns
            -------
        """
        self.ser.write(b'la on\r\n')

    def setLaserOFF(self):
        """ Deactivate LD driver

            Parameters
            ----------
            Returns
            -------
        """
        self.ser.write(b'la off\r\n')

    def getLaserPowerIn_uW(self):
        """ Returns actual laser power in micro watts

            Parameters
            ----------
            Returns
            -------
            power : str
        """
        self.ser.write(b'sh pow\r\n')
        #power = ser.read_until("CMD>")
        power = self.getTerminalString()
        #power_str = str(power, 'utf-8')
        print(power)
        return power

    def getLaserTemp(self):
        """ Returns actual LD temperature

            Parameters
            ----------
            None.

            Returns
            -------
            temp : str

        """
        self.ser.write(b'sh temp\r\n')
        #temp = ser.read_until("CMD>")
        #temp = ser.read(256)
        temp = self.getTerminalString()
        #temp = str(temp, 'utf-8')
        print('Laser Temperature: \r\n' + temp)
        return temp

    def getLaserStatus(self):
        """ Returns actual status of the LD driver

            Parameters
            ----------
            None.

            Returns
            -------
            status : str
                Status of the LD driver
        """
        self.ser.write(b'sta la\r\n')
        #status = ser.read(256)
        status = self.getTerminalString()
        #status_str = str(status, 'utf-8')
        print(status)
        return status

    def initLaser(self):
        ''' Initialize Laser.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'ini la\r\n')

    def enbleChannel(self, channel):
        ''' Enables a certain channel

        Parameters
        ----------
        channel : int
            Channel to enable [1..2].

        Returns
        -------
        None.

        '''
        channel = bytes(channel, encoding='utf-8')
        self.ser.write(b'en ' + channel + b'\r\n')

    def disableAllChannels(self):
        ''' Disables all Channels of the iBeam

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'di 0\r\n')

    def disableChannel(self, channel):
        ''' Disables a certain channel

        Parameters
        ----------
        channel : int
            Channel to diable [1..2].

        Returns
        -------
        None.

        '''
        channel = bytes(channel, encoding='utf-8')
        self.ser.write(b'di ' + channel + b'\r\n')

    def getChannelInfo(self):
        """ Show info of available channels

            Parameters
            ----------
            Returns
            -------
            info : str
        """
        self.ser.write(b'sh ch\r\n')
        #info = ser.read_until("CMD>")
        info = self.getTerminalString()
        #info = str(info, 'utf-8')
        print(info)
        return info

    def setAutopulseByFrequency(self, IO = 1, channel1power = 1.0, freq = 50, duty = 50):
        ''' Sets the Autopulse feature by frequency and duty cycle.
            Afterwards laser is off.

        Parameters
        ----------
        IO : int, optional
            Autopulse On/Off (1/0). The default is 1.
        channel1power : float, optional
            Sets the power of channel 1 in mW. The default is 1.0.
        freq : int, optional
            Sets the frequency of the self-generated pulses in Hz (input "1e6" for 1 MHz allowed). The default is 50.
        duty : int, optional
            Sets the duty cycle of the pulse stream in %. The default is 50.

        Returns
        -------
        status : str
            Status of the Autopulse feature (On/Off).
        '''
        if (IO == 1):
            self.ser.write(b'ch 2 pow 0\r\n')
            self.ser.write(b'ch 1 pow ' + bytes(channel1power, encoding = 'utf-8') + b'\r\n')
            self.ser.write(b'pulse freq ' + bytes(freq, encoding = 'utf-8') + b'\r\n')
            self.ser.write(b'pulse duty ' + bytes(duty, encoding = 'utf-8') + b'\r\n')
            self.ser.write(b'pulse on\r\n')
        else:
            self.ser.write(b'pulse off\r\n')
        status = self.getAutopulseStatus()
        print('Autopulse is set ' + status + '\n')
        if status == 'ON':
            print('with \n')
            print('\tChannel1 Power:\t' + channel1power)
            print('\tFrequency:\t' + freq)
            print('\tDuty Cycle:\t' + duty)
        return status

    #def setAutopulseByFrequency(ser, IO = 1, channel1power = 1.0, )

    def setAutopulse_ON(self):
        '''Turn on Autopulse.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'pulse on\r\n')

    def setAutopulse_OFF(self):
        '''Turn off Autopulse.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'pulse off\r\n')

    def setAutopulse_freq(self, freq):
        '''Set the frequency parameter of the autopulse feature.

        Parameters
        ----------
        freq : int.
            Frequency of Autopulse in Hz. (Inputs such as "1e6" for 1MHz are allowed)

        Returns
        -------
        None.

        '''
        self.ser.write(b'pulse freq ' + bytes(freq, encoding = 'utf-8') + '\r\n')

    def setAutopulse_duty(self, duty):
        '''Set the duty cycle parameter of the autopulse feature.

        Parameters
        ----------
        duty : int.
            Duty cycle of Autopulse in %.

        Returns
        -------
        None.

        '''
        self.ser.write(b'pulse duty ' + bytes(duty, encoding = 'utf-8') + '\r\n')

    def setAutopulse_per(self, per):
        '''Set the periode parameter of the autopulse feature.

        Parameters
        ----------
        per : int.
            Periode of Autopulse in microseconds.

        Returns
        -------
        None.

        '''
        self.ser.write(b'pulse per ' + bytes(per, encoding = 'utf-8') + '\r\n')

    def setAutopulse_width(self, width):
        '''Set the width parameter of the autopulse feature.

        Parameters
        ----------
        width : int.
            Width of Autopulse in microseconds.

        Returns
        -------
        None.

        '''
        self.ser.write(b'pulse width ' + bytes(width, encoding = 'utf-8') + '\r\n')

    def getAutopulseStatus(self):
        self.ser.write(b'sta puls\r\n')
        status = self.getTerminalString()
        return status

    def setFine(self, IO = 1, channel1power = 1.0, paramA = 80, paramB = 10):
        ''' Sets the FINE feature of the iBeam.
            (FINE can only be used with channel 1)

        Parameters
        ----------
        IO : int, optional
            FINE feature On/Off (1/0). The default is 1.
        channel1power : float, optional
            Sets the power of channel 1 in mW. The default is 1.0.
        paramA : int, optional
            Sets the fine parameter "a" in %. The default is 80.
        paramB : int, optional
            Sets the fine parameter "b" in %. The default is 10.

        Returns
        -------
        status : str
            Status of the FINE feature (On/Off).

        '''
        if (IO == 1):
            self.ser.write(b'ch 2 pow 0\r\n')
            self.ser.write(b'ch 1 pow ' + bytes(channel1power, encoding = 'utf-8') + '\r\n')
            self.ser.write(b'fine a 0\r\n')
            self.ser.write(b'fine on\r\n')
            self.ser.write(b'fine a ' + bytes(paramA, encoding = 'utf-8') + '\r\n')
            self.ser.write(b'fine b ' + bytes(paramB, encoding = 'utf-8') + '\r\n')
        else:
            self.ser.write(b'fine off\r\n')
        status = self.getFineStatus()
        print('FINE is set ' + status + '\n')
        if status == 'ON':
            print('with \n')
            print('\tChannel1 Power:\t' + channel1power)
            print('\tParameter A:\t' + paramA)
            print('\tParameter B:\t' + paramB)
        return status

    def setFine_ON(self):
        ''' enable FINE

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'fine on\r\n')

    def setFine_OFF(self):
        ''' disable fine

        Parameters
        ----------
        None

        Returns
        -------
        None.

        '''
        self.ser.write(b'fine off\r\n')

    def setFine_A(self, paramA):
        ''' setting FINE parameter a

        Parameters
        ----------
        paramA : int.
            The a parameter of the FINE feature.

        Returns
        -------
        None.

        '''
        self.ser.write(b'fine a ' + bytes(paramA, encoding ='utf-8') + '\r\n')

    def setFine_B(self, paramB):
        ''' setting FINE parameter a

        Parameters
        ----------
        paramB : int.
            The b parameter of the FINE feature.

        Returns
        -------
        None.

        '''
        self.ser.write(b'fine b ' + bytes(paramB, encoding ='utf-8') + '\r\n')

    def getFineStatus(self):
        self.ser.write(b'sta fine\r\n')
        status = self.getTerminalString()
        return status

    def setSkill(self, IO = 1, channel1power = 1.0, freq = 80, gain = 10):
        ''' Sets the SKILL feature of the iBeam.
            (SKILL can only be used with channel 1)

        Parameters
        ----------
        IO : int, optional
            SKILL feature On/Off (1/0). The default is 1.
        channel1power : float, optional
            Sets the power of channel 1 in mW. The default is 1.0.
        freq : int, optional
            Sets the frequency parameter of the SKILL feature in Hz. The default is 80.
        gain : int, optional
            Sets the gain parameter of the SKILL feature in dBm. The default is 10.

        Returns
        -------
        status : str
            Status of the FINE feature (On/Off).

        '''
        if (IO == 1):
            self.ser.write(b'ch 2 pow 0\r\n')
            self.ser.write(b'ch 1 pow ' + bytes(channel1power, encoding = 'utf-8') + '\r\n')
            self.ser.write(b'skill on\r\n')
            self.ser.write(b'skill freq ' + bytes(freq, encoding = 'utf-8') + '\r\n')
            self.ser.write(b'skill gain ' + bytes(gain, encoding = 'utf-8') + '\r\n')
        else:
            self.ser.write(b'skill off\r\n')
        status = self.getSkillStatus()
        print('SKILL is set ' + status + '\n')
        if status == 'ON':
            print('with \n')
            print('\tChannel1 Power:\t' + channel1power)
            print('\tFrequency:\t' + freq)
            print('\tGain:\t' + gain)
        return status

    def setSkill_ON(self):
        ''' enable SKILL

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'skill on\r\n')

    def setSkill_OFF(self):
        ''' disable SKILL

        Parameters
        ----------
        None

        Returns
        -------
        None.

        '''
        self.ser.write(b'skill off\r\n')

    def setSkill_gain(self, gain):
        ''' setting gain parameter of SKILL feature

        Parameters
        ----------
        gain : int.
            The gain parameter of the SKILL feature.

        Returns
        -------
        None.

        '''
        self.ser.write(b'skill gain ' + bytes(gain, encoding ='utf-8') + '\r\n')

    def setSkill_freq(self, freq):
        ''' setting the frequency parameter of SKILL feature.

        Parameters
        ----------
        freq : int.
            The frequency parameter of the SKILL feature.

        Returns
        -------
        None.

        '''
        self.ser.write(b'skill freq ' + bytes(freq, encoding ='utf-8') + '\r\n')

    def getSkillStatus(self):
        self.ser.write(b'sta skill\r\n')
        status = self.getTerminalString()
        return status

    # =============================================================================
    #   System Control
    # =============================================================================

    def getSystemTemp(self):
        """ Show base plate (heatsink) temperature

            Parameters
            ----------
            Returns
            -------
            temp : str
        """
        self.ser.write(b'sh temp sys\r\n')
        #temp = ser.read(256)
        temp = self.getTerminalString()
        print('Device Temperature: ' + temp)
        return temp

    def ResetSystem(self):
        """ Starts system reboot of the iBeam.

            Parameters
            ----------
            None.

            Returns
            -------
            None.

        """

        self.ser.write(b'reset sys\r\n')
        print('Rebooting Laser')

    def setEcho_ON(self):
        ''' enable echoing of characters sent from host within command entry.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'echo on\r\n')

    def setEcho_OFF(self):
        ''' disable echoing of characters sent from host within command entry.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'echo off\r\n')

    def getLastError(self):
        ''' Shows last Error occured

        Parameters
        ----------

        Returns
        -------
        None.

        '''
        self.ser.write(b'err\r\n')
        err = self.getTerminalString()
        print('Last Error: ' + err)

    def getErrorList(self):
        ''' List error table

        Parameters
        ----------
        None.

        Returns
        -------
        err_list : str
            list of errors.

        '''
        self.ser.write(b'list err\r\n')
        err_list = self.getTerminalString()
        print(err_list)
        return err_list

    def getError(self, number):
        ''' Show text of error number

        Parameters
        ----------
        number : int
            Number of Error.

        Returns
        -------
        err_msg : str
            Error text.

        '''
        self.ser.write(b'list err ' + number + '\r\n')
        err_msg = self.getTerminalString()
        print(err_msg)
        return err_msg

    def getHelp(self):
        ''' Show part of possible command specified by a mask.

        Parameters
        ----------
        None.

        Returns
        -------
        ret : string
            Returns the output of the 'help' command

        '''
        self.ser.write(b'help\r\n')
        ret = self.getTerminalString()
        print(ret)
        return ret

    def getHelp_All(self):
        ''' Show complete list of possible commands for active password level.

        Parameters
        ----------
        None.

        Returns
        -------
        ret : TYPE
            Returns the output of the 'help all' command.

        '''
        self.ser.write(b'help all\r\n')
        ret = self.getTerminalString()
        print(ret)
        return ret

    def getID(self):
        ''' shows identifier or serial number (same as getSerialNumber)

        Parameters
        ----------
        None.

        Returns
        -------
        ID : str
            ID of iBeam.

        '''
        self.ser.write(b'id\r\n')
        ID = self.getTerminalString()
        print(ID)
        return ID

    def initDAC(self):
        ''' initialize DAC and EPOT hardware from RAM table.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        self.ser.write(b'ini da\r\n')

    def resetPassword(self):
        ''' Reset password level to locked state or normal command entry

        Parameters
        ----------
        ser : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.ser.write(b'pass reset')

    #def

    # =============================================================================
    #   Other useful functions
    # =============================================================================
    def CheckForError(terminalString):
        """ Checks if the output of the terminal string contains an error.

        Parameters
        ----------
        terminalString : string
            String from terminal output.

        Returns
        -------
        ret : bool
            True if Error occured, False if no error.

        """
        if "%SYS" in terminalString :
            ret = True
            return ret
        else:
            ret = False
            return ret

    def OutputToError(terminalString):
        """ Convert the eroor output of the terminal to a string containing only
            the errorcode and message.

        Parameters
        ----------
        terminalString : string
            String from terminal output.

        Returns
        -------
        None.

        """
        if "%SYS" in terminalString :
            start_num = terminalString.find("%", 0, len(terminalString))
            end_num = terminalString.find(",", 0, len(terminalString))
            errornumber = terminalString[start_num+1:end_num]
            start_str = terminalString.find(",", start_num, len(terminalString))
            end_str = terminalString.find("\r", start_num, len(terminalString))
            errorstring = terminalString[start_str+2:end_str]

            return [errornumber, errorstring]
        else:
            return "No Error"

    def getTerminalString2(self):
        """

        Parameters
        ----------

        Returns
        -------
        out : string
            Output of the terminal.
        """
        #   Version 1
        #---------------------
        out = b''
        time.sleep(1)
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)


        #   Version 2
        #---------------------
        # out = ser.read(800)


        #   Version 2.1
        #---------------------
        # ser.inWaiting()
        # out = ser.read(800)

        #   Version 3
        #---------------------
        # out = ser.read_until(b'CMD')

        out = str(out, 'utf-8')
        return out

    def getTerminalString(self, chunk_size=200):
        """Read all characters on the serial port and return them."""
        if not self.ser.timeout:
            raise TypeError('Port needs to have a timeout set!')

        read_buffer = b''

        while True:
            # Read in chunks. Each chunk will wait as long as specified by
            # timeout. Increase chunk_size to fail quicker
            byte_chunk = self.ser.read(size=chunk_size)
            read_buffer += byte_chunk
            if not len(byte_chunk) == chunk_size:
                break
        read_buffer = str(read_buffer, 'utf-8')
        read_buffer = read_buffer[0:len(read_buffer)-5]
        return read_buffer

    def write(self, string):
        ''' sends individual command to Laser

        Parameters
        ----------
        String.

        Returns
        -------
        ret : str
            Return of iBeam.

        '''
        self.ser.write(b'' + bytes(string, encoding ='utf-8') + b'\r\n')
        ret = self.getTerminalString()
        print(ret)
        return ret


    def TerminalOutputToList(terminalString):
        """ Converts the terminal output to a list.
            Usage for outputs consisting warnings/errors and/or values with units.
                i.e.:
                    %SYS-I-077, scaled
                    PIC  = 000000 uW

        Parameters
        ----------
        terminalString : string
            DESCRIPTION.

        Returns
        -------
        ret : list
            List containing [ReturnValue, ValueUnit, Info/Error/Warning-Code, -String].
            If list value is not existant list value is "None"

        """
        if "%SYS" in terminalString :
            start_err_num = terminalString.find("%", 0, len(terminalString))
            end_err_num = terminalString.find(",", 0, len(terminalString))
            errornumber = terminalString[start_err_num+1:end_err_num]
            start_err_str = terminalString.find(",", start_err_num, len(terminalString))
            end_err_str = terminalString.find("\r", start_err_num, len(terminalString))
            errorstring = terminalString[start_err_str+2:end_err_str]
            err = [errornumber, errorstring]
        else:
            err = ["None","None"]
        if "=" in terminalString:
            start_num = terminalString.find("=", 0, len(terminalString))
            end_num = terminalString.find(" ", start_num+2, len(terminalString))
            valnumber = terminalString[start_num+2:end_num]
            start_str = end_num+1
            end_str = terminalString.find("\r", start_num, len(terminalString))
            valunit = terminalString[start_str:end_str]
            valunit = valunit.replace(" ","")
            val = [valnumber, valunit]
        else:
            val = ["None", "None"]
        return val + err

    def getValue(terminalString):
        ''' If terminalString contains a value - returns value as integer or float
            If terminalString contains NO value - returns '999'

        Parameters
        ----------
        terminalString : TYPE
            DESCRIPTION.

        Returns
        -------
        val : TYPE
            DESCRIPTION.

        '''
        if "=" in terminalString:
            start_num = terminalString.find("=", 0, len(terminalString))
            end_num = terminalString.find(" ", start_num+2, len(terminalString))
            val = terminalString[start_num+2:end_num]
        else:
            val = 999
        return val



