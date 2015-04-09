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
 * @file si_platform_api.h
 *
 * @brief Minimum Platform API function set for SII9679 Driver
 *
 *****************************************************************************/

#ifndef SI_PLATFORM_API_H
#define SI_PLATFORM_API_H

#ifdef __cplusplus
extern "C"{
#endif

/***** #include statements ***************************************************/

#include "si_datatypes.h"


/***** public macro definitions **********************************************/

#define OS_INFINITE_WAIT ((SiiPlatformSemaphore_t) 0-1)
#define OS_NO_WAIT       ((SiiPlatformSemaphore_t) 0)

/***** public type definitions ***********************************************/

typedef enum
{
    SII_PLATFORM_STATUS__SUCCESS,
    SII_PLATFORM_STATUS__ERR_INVALID_PARAM,
    SII_PLATFORM_STATUS__ERR_NOT_AVAIL,
    SII_PLATFORM_STATUS__ERR_FAILED
} SiiPlatformStatus_t;

typedef uint32_t SiiPlatformSemaphore_t;
typedef uint8_t  SiiPlatformDevId_t;

/***** public functions ******************************************************/

/*****************************************************************************/
/**
* @brief Blocking sleep function
*
* This function should not exit until ’mSec?milliseconds of time.
* The SiI9777 host driver uses this function for brief delays (less than 100 milliseconds).
*
* @param[in]  mSec            Number of milliseconds that this function should wait before it returns.
*
******************************************************************************/
extern void SiiPlatformSleepMsec( uint16_t mSec );

/*****************************************************************************/
/**
* @brief Time inquiry in milliseconds
*
* Provides time in milliseconds passed since system was powered up.
*
* @retval       Absolute time in milliseconds started from system power up. 
*
******************************************************************************/
extern uint32_t SiiPlatformTimeMsecQuery( void );

/*****************************************************************************/
/**
* @brief I2C/SPI Data write function
*
* Implements either I2C or SPI write access to the SiI9777 by writing ‘size?bytes to memory
* starting at ‘addr? If multiple devices are present on the platform ‘devId?is used by this
* function to determine which device to access. This function should return ??if all bytes
* are successfully written and should return ?1?if the write fails. 
*
* @param[in]  devId           Hardware device ID passed to ‘Sii9777Create()?
*                             This ID is associated with a physical hardware device
*                             and is allocated by the user when this function is implemented. 
* @param[in]  addr            16 bit address of register.
* @param[in]  pData           Pointer to array of bytes that is required to be written to register ‘addr?
* @param[in]  size            Number of bytes in array that is required to be written to device.
*
* @retval                      0 : Write was successful
*                             -1 : Write has failed
*
******************************************************************************/
extern uint16_t SiiPlatformHostBlockWrite( SiiPlatformDevId_t devId, uint16_t addr, const uint8_t *pData, uint16_t size );

/*****************************************************************************/
/**
* @brief I2C/SPI Data read function
*
* Implements either I2C or SPI read access to the SiI9777 by reading ‘size?bytes from memory
* starting at ‘addr? If multiple devices are present on the platform ‘devId?is used by this
* function to determine which device to access. This function should return ??if all bytes
* are successfully written and should return ?1?if the write fails. 
*
* @param[in]  devId           Hardware device ID passed to ‘Sii9777Create()?
*                             This ID is associated with a physical hardware device
*                             and is allocated by the user when this function is implemented. 
* @param[in]  addr            16 bit address of register.
* @param[in]  pData           Pointer to array of bytes that is required to be read from register ‘addr?
* @param[in]  size            Number of bytes in array that is required to be read from device.
*
* @retval                      0 : Read was successful
*                             -1 : Read has failed
*
******************************************************************************/
extern uint16_t SiiPlatformHostBlockRead( SiiPlatformDevId_t devId, uint16_t addr, uint8_t *pData, uint16_t size );

/*****************************************************************************/
/**
* @brief Device Hardware Reset
*
* Controls level of reset signal connected to device's RST pin.
*
* @param[in]  devId           Hardware device ID passed to ‘Sii9777Create()?
*                             This ID is associated with a physical hardware device
*                             and is allocated by the user when this function is implemented. 
* @param[in]  bOn             Requested level of reset signal:
*                             false : No reset
*                             true  : Active reset
*
******************************************************************************/
extern void SiiPlatformDeviceResetSet( SiiPlatformDevId_t devId, bool_t bOn );

/*****************************************************************************/
/**
* @brief Semaphore-Take wrapper (Obsoleted. Replaced by SiiPlatformSemaphoreTake() )
*
* Optional function for implementing a semaphore function that blocks until either
* ‘SiiPlatformIpcSemaphoreGive()?is called by the Sii9777 host driver or when
* ‘maxBlockTime?expires. This function is called by Sii9777 host driver directly
* after host driver has sent a request to Sii9777 device and is waiting for a
* response from the sii9777 firmware.
* This function is only called if ‘bIpcSemaphore?flag in the Sii9777Config_t
* structure is is set to ‘true? If ‘bIpcSemaphore?is set to ‘false?an empty
* implementation of this function must be provided to avoid linkage errors.
* Please refer ‘Sii9777rx_PortingGuide?for guidance on how to implement.
*
* @param[in]  maxBlockTime    Maximum time in milliseconds that the semaphore remains blocking
*
* @retval                     Describes reason that semaphore stops blocking:
*                             0 : Released by SiiPlatformIpcSemaphoreGive
*                             1 : Released when maxBlockTime expires
*
******************************************************************************/

/*****************************************************************************/
/**
* @brief Semaphore-Give wrapper (Obsoleted. Replaced by SiiPlatformSemaphoreGive() )
*
* Optional function that releases ‘SiiPlatformIpcSemaphoreTake()?from being blocked.
* This function is called by Sii9777 host driver directly after host driver has
* received an acknowledgement to a message from Sii9777 device.
* This function is only called if ‘bIpcSemaphore?flag in the Sii9777Config_t
* structure is is set to ‘true? If ‘bIpcSemaphore?is set to ‘false?an empty
* implementation of this function must be provided to avoid linkage errors. Please
* refer ‘Sii9777rx_PortingGuide?for guidance on how to implement.
*
******************************************************************************/

extern SiiPlatformStatus_t SiiPlatformSemaphoreCreate( const char *pName, uint32_t maxCount, uint32_t initialValue, SiiPlatformSemaphore_t *pSemId );
extern SiiPlatformStatus_t SiiPlatformSemaphoreDelete( SiiPlatformSemaphore_t semId );

/*****************************************************************************/
/**
* @brief Semaphore-Give wrapper
*
* Optional function that releases ‘SiiPlatformIpcSemaphoreTake()?from being blocked.
* This function is called by Sii9777 host driver directly after host driver has
* received an acknowledgement to a message from Sii9777 device.
* This function is only called if ‘bIpcSemaphore?flag in the Sii9777Config_t
* structure is is set to ‘true? If ‘bIpcSemaphore?is set to ‘false?an empty
* implementation of this function must be provided to avoid linkage errors. Please
* refer ‘Sii9777rx_PortingGuide?for guidance on how to implement.
*
******************************************************************************/
extern SiiPlatformStatus_t SiiPlatformSemaphoreGive( SiiPlatformSemaphore_t semId );

/*****************************************************************************/
/**
* @brief Semaphore-Take wrapper
*
* Optional function for implementing a semaphore function that blocks until either
* ‘SiiPlatformIpcSemaphoreGive()?is called by the Sii9777 host driver or when
* ‘maxBlockTime?expires. This function is called by Sii9777 host driver directly
* after host driver has sent a request to Sii9777 device and is waiting for a
* response from the sii9777 firmware.
* This function is only called if ‘bIpcSemaphore?flag in the Sii9777Config_t
* structure is is set to ‘true? If ‘bIpcSemaphore?is set to ‘false?an empty
* implementation of this function must be provided to avoid linkage errors.
* Please refer ‘Sii9777rx_PortingGuide?for guidance on how to implement.
*
* @param[in]  maxBlockTime    Maximum time in milliseconds that the semaphore remains blocking
*
* @retval                     Describes reason that semaphore stops blocking:
*                             0 : Released by SiiPlatformIpcSemaphoreGive
*                             1 : Released when maxBlockTime expires
*
******************************************************************************/
extern SiiPlatformStatus_t SiiPlatformSemaphoreTake( SiiPlatformSemaphore_t semId, int32_t timeMsec );

/*****************************************************************************/
/**
* @brief ASCII string logger
*
* Function for outputting NULL terminated log strings to a platform specific
* logging mechanism such as a UART or log file. 
*
* @param[in]  pStr    Pointer to string to be logged.
*
******************************************************************************/
extern void SiiPlatformLogPrint( const char* pStr );

extern bool_t SiiPlatformCreate(int port);
extern bool_t SiiPlatformInterruptQuery(int port);
extern void SiiPlatformDelete(int port);

#ifdef __cplusplus
}
#endif

#endif // SI_PLATFORM_API_H
