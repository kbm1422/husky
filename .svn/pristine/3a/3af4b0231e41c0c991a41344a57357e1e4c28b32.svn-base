/******************************************************************************
 *
 * Copyright 2013, Silicon Image, Inc.  All rights reserved.
 * No part of this work may be reproduced, modified, distributed, transmitted,
 * transcribed, or translated into any language or computer format, in any form
 * or by any means without written permission of
 * Silicon Image, Inc., 1140 East Arques Avenue, Sunnyvale, California 94085
 *
 *****************************************************************************/
/**
 * @file reg_access.c
 *
 * @brief register access APIs
 *
 *****************************************************************************/

/***** #include statements ***************************************************/

#include <conio.h>
#include <stdio.h>
#include <windows.h>
#include <sys/stat.h>

#include "si_hal_aardvark_api.h"
#include "aardvark.h"
#include "si_datatypes.h"

/***** local macro definitions ***********************************************/

#define I2C_SLAVE_ADDR              0x40    /* this is for "Boston" only */
#define MAX_NUM_ADAPTORS            10
#define I2C_BITRATE                 400


#define GPIO_HW_RESET				AA_GPIO_SS
#define GPIO_HW_RESET_ASSERTED		0x00
#define GPIO_HW_RESET_DEASSERTED	AA_GPIO_SS

#define GPIO_HW_INT			        AA_GPIO_MISO

#define BUS_STRING                  "I2C "

/***** local type definitions ************************************************/

enum reg_access_status
{
    REG_ACCESS_OK,
    REG_ACCESS_ERROR
};


/***** local data objects ****************************************************/

SiiHalAardvarkHostBus_t sHostBus      = SII_HAL_AARDVARK_HOST_BUS__I2C;
uint8_t                 sI2cSlaveAddr = I2C_SLAVE_ADDR;

/***** public functions ******************************************************/

Aardvark SiiHalAardvarkCreate(int port)
{
	Aardvark i2cHandle = aa_open(port);
	aa_configure(i2cHandle, AA_CONFIG_GPIO_I2C);
	aa_i2c_pullup(i2cHandle, AA_I2C_PULLUP_NONE);
	aa_target_power(i2cHandle, AA_TARGET_POWER_NONE);

	// Setup the bitrate
	aa_i2c_bitrate(i2cHandle, I2C_BITRATE);

	// Set GPIO direction (of HW_RESET) to output.
	aa_gpio_set(i2cHandle, GPIO_HW_RESET_DEASSERTED);
	aa_gpio_direction(i2cHandle, GPIO_HW_RESET);
	return i2cHandle;

}

void SiiHalAardvarkDelete(Aardvark i2cHandle)
{
	if( i2cHandle > 0 )
	{
		aa_close(i2cHandle);
	}
}

//------------------------------------------------------------------------------
// Function:    SiiHalAardvarkHostBusSet
// Description: Select host bus interface on Aardvark device: I2C or SPI.
//------------------------------------------------------------------------------
void SiiHalAardvarkHostBusSet( SiiHalAardvarkHostBus_t hostBus )
{
    sHostBus = hostBus;
}

//------------------------------------------------------------------------------
// Function:    SiiHalAardvarkI2cSlaveAddressSet
// Description: Select I2C slave device address.
//------------------------------------------------------------------------------
void SiiHalAardvarkI2cSlaveAddressSet( uint8_t slaveAddr )
{
    sI2cSlaveAddr = slaveAddr;
}

//------------------------------------------------------------------------------
// Function:    SiiHalI2CReadBlock
// Description: Reads a block of data from sequential registers.
//
// A count of 0 will read 256 bytes.
//------------------------------------------------------------------------------
int SiiHalAardvarkBlockRead(Aardvark i2cHandle, uint16_t offset, uint8_t *buffer, uint16_t count)
{
	int      status;
	uint8_t  data[2];
	uint16_t num_bytes;

	data[0] = (offset >> 8) & 0xFF;
	data[1] = offset & 0xFF;
	
	status = aa_i2c_write_ext(i2cHandle, (unsigned short)(sI2cSlaveAddr >> 1), AA_I2C_NO_STOP, 2, data, (unsigned short *)&num_bytes);
	if (status == REG_ACCESS_OK)
	{
		status = aa_i2c_read_ext(i2cHandle, (unsigned short)(sI2cSlaveAddr >> 1), AA_I2C_NO_FLAGS, count, buffer, (unsigned short *)&num_bytes);
	}

	if (status != REG_ACCESS_OK)
	{
		status = REG_ACCESS_ERROR;
	}

    return status;
}

//------------------------------------------------------------------------------
// Function:    reg_write_block
// Description: Writes a block of data to sequential registers.
//------------------------------------------------------------------------------
int SiiHalAardvarkBlockWrite(Aardvark i2cHandle, uint16_t offset, const uint8_t *buffer, uint16_t count)
{
	int      status;
	uint16_t i;
	uint8_t  data[1024];
	uint16_t num_bytes;

	i = 0;
	data[i++] = (offset >> 8) & 0xFF;
	data[i++] = offset & 0xFF;

	for (;i <= count + 1; i++)
	{
		data[i] = buffer[i - 2];
	}

	status = aa_i2c_write_ext(i2cHandle, (unsigned short)(sI2cSlaveAddr >> 1), AA_I2C_NO_FLAGS, i, data, (unsigned short *)&num_bytes);

	if (status != REG_ACCESS_OK)
	{
		status = REG_ACCESS_ERROR;
	}

    return status;
}

//------------------------------------------------------------------------------
// Function:    SiiHalAardvarkInterruptQuery
// Description: return the interrupt pin status.
//------------------------------------------------------------------------------
bool_t SiiHalAardvarkInterruptQuery(Aardvark i2cHandle)
{
	return ((aa_gpio_get(i2cHandle) & GPIO_HW_INT) == 0x00);
}

//------------------------------------------------------------------------------
// Function:    SiiHalAardvarkDeviceResetSet
// Description: Reset the chip using the GPIO chip select
//------------------------------------------------------------------------------
void SiiHalAardvarkDeviceResetSet(Aardvark i2cHandle, bool_t bOn)
{
    if( bOn )
    {
        // Keep FW_WAKE deasserted, assert HW_RESET.
        aa_gpio_set(i2cHandle, GPIO_HW_RESET_ASSERTED);
    }
    else
    {
        // Keep FW_WAKE deasserted, deassert HW_RESET.
    	aa_gpio_set(i2cHandle, GPIO_HW_RESET_DEASSERTED);
    }
}