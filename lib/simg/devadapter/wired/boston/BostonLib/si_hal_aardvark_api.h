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
 * @file si_hal_i2c_api.h
 *
 * @brief register access APIs
 *
 *****************************************************************************/

#ifndef SI_HAL_I2C_API_H
#define SI_HAL_I2C_API_H

/***** #include statements ***************************************************/

#include "aardvark.h"
#include "si_datatypes.h"


/***** local type definitions ************************************************/

typedef enum
{
    SII_HAL_AARDVARK_HOST_BUS__I2C,
    SII_HAL_AARDVARK_HOST_BUS__SPI   // Currently not supported
} SiiHalAardvarkHostBus_t;

/***** public functions ******************************************************/

Aardvark SiiHalAardvarkCreate( int port );
void SiiHalAardvarkDelete( Aardvark i2cHandle );

void SiiHalAardvarkHostBusSet( SiiHalAardvarkHostBus_t hostBus );
void SiiHalAardvarkI2cSlaveAddressSet( uint8_t slaveAddr );

int SiiHalAardvarkBlockRead( Aardvark i2cHandle, uint16_t offset, uint8_t *buffer, uint16_t count );
int SiiHalAardvarkBlockWrite( Aardvark i2cHandle, uint16_t offset, const uint8_t *buffer, uint16_t count );

bool_t SiiHalAardvarkInterruptQuery( Aardvark i2cHandle );
void SiiHalAardvarkDeviceResetSet( Aardvark i2cHandle, bool_t bOn);

#endif //SI_HAL_I2C_API_H

/***** end of file ***********************************************************/
