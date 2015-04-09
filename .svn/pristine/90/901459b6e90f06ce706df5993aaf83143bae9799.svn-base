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
 * file si_platform.c
 *
 * @brief SII9679 platform implementation example
 *
 *****************************************************************************/

/***** #include statements ***************************************************/

#include <time.h>
#include <windows.h>
#include "si_datatypes.h"
#include "sii9777_platform_api.h"
#include "si_hal_aardvark_api.h"

/***** local macro definitions ***********************************************/

/***** public functions ******************************************************/
Aardvark i2cHandles[10];

bool_t SiiPlatformCreate(int port) 
{
	Aardvark i2cHandle = SiiHalAardvarkCreate(port);
	if(i2cHandle>0)
	{
		i2cHandles[port] = i2cHandle;
		return true;
	}
	return false;
}

void SiiPlatformDelete(int port)
{
	SiiHalAardvarkDelete(i2cHandles[port]);
}

bool_t SiiPlatformInterruptQuery(int port)
{
	return SiiHalAardvarkInterruptQuery(i2cHandles[port]);
}

void SiiPlatformSleepMsec( uint16_t mSec )
{
    Sleep(mSec);
}

uint32_t SiiPlatformTimeMsecQuery( void )
{
    return clock();
}

uint16_t SiiPlatformHostBlockWrite( SiiPlatformDevId_t devId, uint16_t addr, const uint8_t *pData, uint16_t size )
{
    switch( devId )
    {
        default :
            SiiHalAardvarkI2cSlaveAddressSet(0x40);
            break;
    }
	return (uint16_t)SiiHalAardvarkBlockWrite(i2cHandles[devId], addr, pData, size);
}

uint16_t SiiPlatformHostBlockRead( SiiPlatformDevId_t devId, uint16_t addr, uint8_t *pData, uint16_t size )
{
    switch( devId )
    {
        default :
            SiiHalAardvarkI2cSlaveAddressSet(0x40);
            break;
    }
	return (uint16_t)SiiHalAardvarkBlockRead(i2cHandles[devId], addr, pData, size);
}

void SiiPlatformDeviceResetSet( SiiPlatformDevId_t devId, bool_t bOn )
{
    devId = devId;
    /* Note for supporting multiple Sii9777 devives through one Aardvark interface:                             */
    /* Since Aardvark supports only one reset signal all Sii9777 devices must be connected to this reset signal */ 
	SiiHalAardvarkDeviceResetSet(i2cHandles[devId], bOn);
}

SiiPlatformStatus_t SiiPlatformSemaphoreCreate( const char *pName, uint32_t maxCount, uint32_t initialValue, SiiPlatformSemaphore_t *pSemId )
{
    pName = pName;
    maxCount = maxCount;
    initialValue = initialValue;
    pSemId = pSemId;
    return SII_PLATFORM_STATUS__SUCCESS;
}

SiiPlatformStatus_t SiiPlatformSemaphoreDelete( SiiPlatformSemaphore_t semId )
{
    semId = semId;
    return SII_PLATFORM_STATUS__SUCCESS;
}

SiiPlatformStatus_t SiiPlatformSemaphoreGive( SiiPlatformSemaphore_t semId )
{
    semId = semId;
    return SII_PLATFORM_STATUS__SUCCESS;
}

SiiPlatformStatus_t SiiPlatformSemaphoreTake( SiiPlatformSemaphore_t semId, int32_t timeMsec )
{
    semId = semId;
    timeMsec = timeMsec;
    return SII_PLATFORM_STATUS__SUCCESS;
}

void SiiPlatformLogPrint( const char* pStr )
{
//    pStr = pStr;
    printf(pStr);
}

void SiiPlatformAssert( const char* pFileStr, uint32_t lineNo )
{
    char lineNoStr[20];

    SII_SPRINTF(lineNoStr, "%ld", lineNo);

    printf("Assertion Failure in ", 0);
    printf((char*)pFileStr, 0);
    printf(" at line no ", 0);
    printf(lineNoStr, 0);
    printf("\n", 0);
    { uint8_t i=1; while(i); }
}

/***** end of file ***********************************************************/
