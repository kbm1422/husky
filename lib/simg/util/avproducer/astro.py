#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

import socket
import collections


class VGError(Exception):
    pass


class VGUnexpectedResponseChar(VGError):
    pass


class VGErrorResponse(VGError):
    pass


class VG876(object):
    # Externally visible supported timings.
    # The Names are visible for documentation, but the Values are private.
    # These dictionaries should be considered READ_ONLY.
    # Internal dictionaries are derived from these initial values.

    supported_video_programs = {
        'EIA640x480p@59.94': '1001',
        'EIA640x480p@60': '1002',
        'EIA720x480p@59.94': '1003',
        'EIA720x480p@60': '1004',
        'EIA720x480pW@59.94': '1005',
        'EIA720x480pW@60': '1006',
        'EIA1280x720p@59.94': '1007',
        'EIA1280x720p@60': '1008',
        'EIA1920x1080i@59.94': '1009',
        'EIA1920x1080i@60': '1010',
        'EIA1440x480i@59.94': '1011',
        'EIA1440x480i@60': '1012',
        'EIA1440x480iW@59.94': '1013',
        'EIA1440x480iW@60': '1014',
        'EIA1440x240p@59.94': '1015',
        'EIA1440x240p@60': '1016',
        # 'EIA1440x240p@59.94': '1017',
        # 'EIA1440x240p@60': '1018',
        'EIA1440x240pW@59.94': '1019',
        'EIA1440x240pW@60': '1020',
        # 'EIA1440x240pW@59.94': '1021',
        # 'EIA1440x240pW@60': '1022',
        'EIA2880x480i@59.94': '1023',
        'EIA2880x480i@60': '1024',
        'EIA2880x480iW@59.94': '1025',
        'EIA2880x480iW@60': '1026',
        'EIA2880x240p@59.94': '1027',
        'EIA2880x240p@60': '1028',
        # 'EIA2880x240p@59.94': '1029',
        # 'EIA2880x240p@59.94': '1030',
        'EIA2880x240pW@59.94': '1031',
        'EIA2880x240pW@60': '1032',
        # 'EIA2880x240pW@59.94': '1033',
        # 'EIA2880x240pW@60': '1034',
        'EIA1440x480p@59.94': '1035',
        'EIA1440x480p@60': '1036',
        'EIA1440x480pW@59.94': '1037',
        'EIA1440x480pW@60': '1038',
        'EIA1920x1080p@59.94': '1039',
        'EIA1920x1080p@60': '1040',
        'EIA720x576p@50': '1041',
        'EIA720x576pW@50': '1042',
        'EIA1280x720p@50': '1043',
        'EIA1920x1080i@50': '1044',
        'EIA1440x576i@50': '1045',
        'EIA1440x576iW@50': '1046',
        'EIA1440x288p@50': '1047',
        # 'EIA1440x288p@50': '1048',
        # 'EIA1440x288p@50': '1049',
        'EIA1440x288pW@50': '1050',
        # 'EIA1440x288pW@50': '1051',
        # 'EIA1440x288pW@50': '1052',
        'EIA2880x576i@50': '1053',
        'EIA2880x576iW@50': '1054',
        'EIA2880x288p@50': '1055',
        # 'EIA2880x288p@50': '1056',
        # 'EIA2880x288p@50': '1057',
        'EIA2880x288pW@50': '1058',
        # 'EIA2880x288pW@50': '1059',
        # 'EIA2880x288pW@50': '1060',
        'EIA1440x576p@50': '1061',
        'EIA1440x576pW@50': '1062',
        'EIA1920x1080p@50': '1063',
        'EIA1920x1080p@23.97': '1064',
        'EIA1920x1080p@24': '1065',
        'EIA1920x1080p@25': '1066',
        'EIA1920x1080p@29.97': '1067',
        'EIA1920x1080p@30': '1068',
        'EIA2880x480p@59.94': '1069',
        'EIA2880x480p@60': '1070',
        'EIA2880x480pW@59.94': '1071',
        'EIA2880x480pW@60': '1072',
        'EIA2880x576p@50': '1073',
        'EIA2880x576pW@50': '1074',
        # 'EIA1920x1080i@50': '1075',
        'EIA1920x1080i@100': '1076',
        'EIA1280x720p@100': '1077',
        'EIA720x576p@100': '1078',
        'EIA720x576pW@100': '1079',
        'EIA1440x576i@100': '1080',
        'EIA1440x576iW@100': '1081',
        'EIA1920x1080i@119.88': '1082',
        'EIA1920x1080i@120': '1083',
        'EIA1280x720p@119.88': '1084',
        'EIA1280x720p@120': '1085',
        'EIA720x480p@119.88': '1086',
        'EIA720x480p@120': '1087',
        'EIA720x480pW@119.88': '1088',
        'EIA720x480pW@120': '1089',
        'EIA1440x480i@119.88': '1090',
        'EIA1440x480i@120': '1091',
        'EIA1440x480iW@119.88': '1092',
        'EIA1440x480iW@120': '1093',
        'EIA720x576p@200': '1094',
        'EIA720x576pW@200': '1095',
        'EIA1440x576i@200': '1096',
        'EIA1440x576iW@200': '1097',
        'EIA720x480p@239.76': '1098',
        'EIA720x480p@240': '1099',
        'EIA720x480pW@239.76': '1100',
        'EIA720x480pW@240': '1101',
        'EIA1440x480i@239.76': '1102',
        'EIA1440x480i@240': '1103',
        'EIA1440x480iW@239.76': '1104',
        'EIA1440x480iW@240': '1105',
        'EIA1280x720p@24': '1106',
        'EIA1280x720p@25': '1107',
        'EIA1280x720p@30': '1108',
        'EIA1920x1080p@100': '1109',
        'EIA1920x1080p@120': '1110',
        'EIA480p59-YCC-12': '1151',
        'EIA1080i59-YCC-12': '1152',
        'EIA720p59-YCC-12': '1153',
        # 'EIA480p59-YCC-12': '1154',
        'EIA1080p59-YCC-12': '1155',
        'EIA480i59-YCC-12': '1156',
        'EIA1080p24-YCC-12': '1157',
        'EIA576p50-YCC-12': '1158',
        'EIA1080i50-YCC-12': '1159',
        'EIA720p50-YCC-12': '1160',
        'EIA480p59-RGB-12': '1171',
        'EIA1080i59-RGB-12': '1172',
        'EIA720p59-RGB-12': '1173',
        # 'EIA480p59-RGB-12': '1174',
        'EIA1080p59-RGB-12': '1175',
        'EIA480i59-RGB-12': '1176',
        'EIA1080p24-RGB-12': '1177',
        'EIA576p50-RGB-12': '1178',
        'EIA1080i50-RGB-12': '1179',
        'EIA720p50-RGB-12': '1180',
        'EIA1080i59-YCC-12-xv': '1191',
        'EIA720p59-YCC-12-xv': '1192',
        'EIA1080p59-YCC-12-xv': '1193',
        'EIA1080p24-YCC-12-xv': '1194',
        'EIA1080i50-YCC-12-xv': '1195',
        'EIA720p50-YCC-12-xv': '1196',
        'EIA1080p50-YCC-12-xv': '1197',
        'EIA1080p25-YCC-12-xv': '1198',
        '3D 1080p60 FramePack': '1201',
        '3D 1080p50 FramePack': '1202',
        '3D 1080p30 FramePack': '1203',
        '3D 1080p24 FramePack': '1204',
        '3D 1080i60 FramePack': '1205',
        '3D 1080i50 FramePack': '1206',
        '3D 720p60 FramePack': '1207',
        '3D 720p50 FramePack': '1208',
        '3D 720p30 FramePack': '1209',
        '3D 720p24 FramePack': '1210',
        '3D 480p60 FramePack': '1211',
        '3D 480i60 FramePack': '1212',
        '3D 576p50 FramePack': '1213',
        '3D 576i50 FramePack': '1214',
        '3D VGAp60 FramePack': '1215',
        '3D 1080p25 FramePack': '1216',
        '3D 1080p60 Side_half': '1221',
        '3D 1080p50 Side_half': '1222',
        '3D 1080p30 Side_half': '1223',
        '3D 1080p24 Side_half': '1224',
        '3D 1080i60 Side_half': '1225',
        '3D 1080i50 Side_half': '1226',
        '3D 720p60 Side_half': '1227',
        '3D 720p50 Side_half': '1228',
        '3D 720p30 Side_half': '1229',
        '3D 720p24 Side_half': '1230',
        '3D 480p60 Side_half': '1231',
        '3D 480i60 Side_half': '1232',
        '3D 576p50 Side_half': '1233',
        '3D 576i50 Side_half': '1234',
        '3D VGAp60 Side_half': '1235',
        '3D 1080p25 Side_half': '1236',
        '3D 1080p60 TopandBot': '1241',
        '3D 1080p50 TopandBot': '1242',
        '3D 1080p30 TopandBot': '1243',
        '3D 1080p24 TopandBot': '1244',
        '3D 1080i60 TopandBot': '1245',
        '3D 1080i50 TopandBot': '1246',
        '3D 720p60 TopandBot': '1247',
        '3D 720p50 TopandBot': '1248',
        '3D 720p30 TopandBot': '1249',
        '3D 720p24 TopandBot': '1250',
        '3D 480p60 TopandBot': '1251',
        '3D 480i60 TopandBot': '1252',
        '3D 576p50 TopandBot': '1253',
        '3D 576i50 TopandBot': '1254',
        '3D VGAp60 TopandBot': '1255',
        '3D 1080p25 TopandBot': '1256',
        '3D 1080p60 Side_full': '1261',
        '3D 1080p50 Side_full': '1262',
        '3D 1080p30 Side_full': '1263',
        '3D 1080p24 Side_full': '1264',
        '3D 1080i60 Side_full': '1265',
        '3D 1080i50 Side_full': '1266',
        '3D 720p60 Side_full': '1267',
        '3D 720p50 Side_full': '1268',
        '3D 720p30 Side_full': '1269',
        '3D 720p24 Side_full': '1270',
        '3D 480p60 Side_full': '1271',
        '3D 480i60 Side_full': '1272',
        '3D 576p50 Side_full': '1273',
        '3D 576i50 Side_full': '1274',
        'SD-SDI 487i@59.94': '1301',
        'SD-SDI 576i@50': '1302',
        '3D VGAp60 Side_full': '1275',
        'HD-SDI 1080@60i': '1311',
        'HD-SDI 1080@59.94i': '1312',
        'HD-SDI 1080@50i': '1313',
        'HD-SDI 1080@30sf': '1314',
        'HD-SDI 1080@29.97sf': '1315',
        'HD-SDI 1080@25sf': '1316',
        'HD-SDI 1080@24sf': '1317',
        'HD-SDI 1080@23.98sf': '1318',
        'HD-SDI 720@60p': '1319',
        'HD-SDI 720@59.94p': '1320',
        'HD-SDI 720@30p': '1321',
        'HD-SDI 720@29.97p': '1322',
        'HD-SDI 720@25p': '1323',
        'HD-SDI 720@24p': '1324',
        'HD-SDI 720@23.98p': '1325',
        'HD-SDI 720@50p': '1326',
        '3G-A 60p YC422 10b': '1331',
        '3G-A 59p YC422 10b': '1332',
        '3G-A 60i RGB 12b': '1333',
        '3G-A 59i RGB 12b': '1334',
        '3G-A 60i YC444 12b': '1335',
        '3G-A 59i YC444 12b': '1336',
        '3G-A 60i YC422 12b': '1337',
        '3G-A 59i YC422 12b': '1338',
        '3G-A DCI RGB 12b': '1339',
        '3G-B 60p YC422 10b': '1341',
        '3G-B 59p YC422 10b': '1342',
        '3G-B 60i RGB 12b': '1343',
        '3G-B 59i RGB 12b': '1344',
        '3G-B 60i YC444 12b': '1345',
        '3G-B 59i YC444 12b': '1346',
        '3G-B 60i YC422 12b': '1347',
        '3G-B 59i YC422 12b': '1348',
        '3G-B DCI RGB 12b': '1349',
        'Dual 60p YC422 10b': '1351',
        'Dual 59p YC422 10b': '1352',
        'Dual 60i RGB 12b': '1353',
        'Dual 59i RGB 12b': '1354',
        'Dual 60i YC444 12b': '1355',
        'Dual 59i YC444 12b': '1356',
        'Dual 60i YC422 12b': '1357',
        'Dual 59i YC422 12b': '1358',
        'Dual DCI RGB 12b': '1359',
        '3G-A 50p YC422 10b': '1361',
        '3G-B 50p YC422 10b': '1362',
        'Dual 50p YC422 10b': '1363',
        '4K2K 3840x2160p60 s0': '1381',
        '4K2K 3840x2160p60 s1': '1382',
        '4K2K 3840x2160p60 s2': '1383',
        '4K2K 3840x2160p60 s3': '1384',
        '4K2K 3840x2160p120s0': '1385',
        '4K2K 3840x2160p120s1': '1386',
        '4K2K 3840x2160p120s2': '1387',
        '4K2K 3840x2160p120s3': '1388',
        '4K2K 3840x2160p30': '1389',
        '4K2K 3840x2160p25': '1390',
        '4K2K 3840x2160p24': '1391',
        '4K2K 4096x2160p24': '1392',
        '4K2K 3840x2160p60 s4': '1393',
        '4K2K 3840x2160p120s4': '1394',
        '4K2K 3840x2160p120s5': '1395',
        '4K2K 3840x2160p120s6': '1396',
        '4K2K 3840x2160p120s7': '1397',
        '4K2K 3840x2160p120s8': '1398',
        '4K2K 3840x2160p120s9': '1399',
        'NTSC PROG.': '1401',
        'NTSC PROG. W': '1402',
        'NTSC PROG. LB': '1403',
        '1920x1080@59.94i': '1404',
        '1920x1080@60i': '1405',
        '1920x1080@59.94p': '1406',
        '1920x1080@60p': '1407',
        '1280x720@59.94p': '1408',
        '1280x720@60p': '1409',
        'NTSC-J 4:3': '1410',
        'PAL PROG.': '1416',
        'PAL PROG. W': '1417',
        'PAL PROG. LB': '1418',
        '1920x1080@50i': '1419',
        '1920x1080@50p': '1420',
        '1280x720@50p': '1421',
        'PAL 4:3': '1422',
        '1920x1080@29.97p': '1426',
        '1920x1080@30p': '1427',
        '1920x1080@23.98p': '1428',
        '1920x1080@24p': '1429',
        '1920x1080@25p': '1430',
        '1920x1080@29.97sf': '1431',
        '1920x1080@30sf': '1432',
        '1920x1080@23.98sf': '1433',
        '1920x1080@24sf': '1434',
        '1920x1080@25sf': '1435',
        '1280x720@29.97p': '1436',
        '1280x720@30p': '1437',
        '1280x720@23.98p': '1438',
        '1280x720@24p': '1439',
        '1280x720@25p': '1440',
        '1920x1035@59.94i': '1451',
        '1920x1035@60i': '1452',
        'SMPTE295Mi': '1453',
        'SMPTE295Mp': '1454',
        'AUS 1152i': '1455',
        'AUS 1080i': '1456',
        # 'NTSC-J 4:3': '1501',
        'NTSC-J 16:9': '1502',
        'NTSC-J LB': '1503',
        # 'PAL 4:3': '1504',
        'PAL 16:9': '1505',
        'PAL LB': '1506',
        'SECAM 4:3': '1507',
        'SECAM 16:9': '1508',
        'SECAM LB': '1509',
        'NTSC-M': '1510',
        'NTSC-443': '1511',
        'PAL-M': '1512',
        'PAL-60': '1513',
        'PAL-N': '1514',
        'PAL-Nc': '1515',
        'Closed Caption CC1': '1521',
        'Closed Caption CC2': '1522',
        'Closed Caption Text1': '1523',
        'Closed Caption Text2': '1524',
        'V Chip MPAA G': '1525',
        'V Chip MPAA X': '1526',
        'V Chip US TV-Y': '1527',
        'V Chip US TV-MA-VSL': '1528',
        'PAL TELETEXT': '1531',
        'Mac NTSC-J DVD Type1': '1541',
        'Mac NTSC-J DVD Type2': '1542',
        'Mac NTSC-J DVD Type3': '1543',
        'Mac PAL DVD': '1544',
        'SCART PAL VBS 4:3': '1551',
        'SCART PAL Y/C 4:3': '1552',
        'SCART PAL RGB 4:3': '1553',
        'SCART PAL VBS 16:9': '1554',
        'SCART PAL TELETEXT': '1555',
        'VESA640x350@85': '1601',
        'VESA640x400@85': '1602',
        'VESA720x400@85': '1603',
        'VESA640x480@60': '1604',
        'VESA640x480@72': '1605',
        'VESA640x480@75': '1606',
        'VESA640x480@85': '1607',
        'VESA800x600@56': '1608',
        'VESA800x600@60': '1609',
        'VESA800x600@72': '1610',
        'VESA800x600@75': '1611',
        'VESA800x600@85': '1612',
        'VESA800x600@120CVT': '1613',
        'VESA848x480@60': '1614',
        'VESA1024x768@43': '1615',
        'VESA1024x768@60': '1616',
        'VESA1024x768@70': '1617',
        'VESA1024x768@75': '1618',
        'VESA1024x768@85': '1619',
        'VESA1024x768@120CVT': '1620',
        'VESA1152x864@75': '1621',
        'VESA1280x768@60CVT': '1622',
        'VESA1280x768@60': '1623',
        'VESA1280x768@75': '1624',
        'VESA1280x768@85': '1625',
        'VESA1280x768@120CVT': '1626',
        'VESA1280x800@60CVT': '1627',
        'VESA1280x800@60': '1628',
        'VESA1280x800@75': '1629',
        'VESA1280x800@85': '1630',
        'VESA1280x800@120CVT': '1631',
        'VESA1280x960@60': '1632',
        'VESA1280x960@85': '1633',
        'VESA1280x960@120CVT': '1634',
        'VESA1280x1024@60': '1635',
        'VESA1280x1024@75': '1636',
        'VESA1280x1024@85': '1637',
        'VESA1280x1024@120CVT': '1638',
        'VESA1360x768@60': '1639',
        'VESA1360x768@120CVT': '1640',
        'VESA1400x1050@60': '1641',
        # 'VESA1400x1050@60': '1642',
        'VESA1400x1050@75': '1643',
        'VESA1400x1050@85': '1644',
        'VESA1400x1050@120CVT': '1645',
        'VESA1440x900@60CVT': '1646',
        'VESA1440x900@60': '1647',
        'VESA1440x900@75': '1648',
        'VESA1440x900@85': '1649',
        'VESA1440x900@120CVT': '1650',
        'VESA1600x1200@60': '1651',
        'VESA1600x1200@65': '1652',
        'VESA1600x1200@70': '1653',
        'VESA1600x1200@75': '1654',
        'VESA1600x1200@85': '1655',
        'VESA1600x1200@120CVT': '1656',
        'VESA1680x1050@60CVT': '1657',
        'VESA1680x1050@60': '1658',
        'VESA1680x1050@75': '1659',
        'VESA1680x1050@85': '1660',
        'VESA1680x1050@120CVT': '1661',
        'VESA1792x1344@60': '1662',
        'VESA1792x1344@75': '1663',
        'VESA1792x1344@120CVT': '1664',
        'VESA1856x1392@60': '1665',
        'VESA1856x1392@75': '1666',
        'VESA1920x1200@60': '1668',
        # 'VESA1920x1200@60': '1669',
        'VESA1920x1200@75': '1670',
        'VESA1920x1200@85': '1671',
        'VESA1920x1200@120CVT': '1672',
        'VESA1920x1440@60': '1673',
        'VESA1920x1440@75': '1674',
        'VESA2560x1600@60CVT': '1676',
        'VESA1366x768@60': '1677',
        'VESA1280x720@60': '1678',
        # 'VESA1366x768@60': '1679',
        'VESA1600x900@60': '1680',
        'VESA1920x1080@60': '1681',
        'VESA2048x1152@60': '1682',
        'VESA1856x1392@120CVT': '1683',
        'VESA1920x1440@120CVT': '1684',
        'VESA2560x1600@60': '1685',
        'VESA2560x1600@75': '1686',
        'VESA2560x1600@85': '1687',
        'VESA2560x1600@120CVT': '1688',
        'VESA4096x2160@60CVT': '1689',
        'VESA4096x2160@59.CVT': '1690',
        'EIA1280x720p@23.98': '1701',
        # 'EIA1280x720p@24': '1702',
        # 'EIA1280x720p@25': '1703',
        'EIA1280x720p@29.97': '1704',
        # 'EIA1280x720p@30': '1705',
        # 'EIA1280x720p@50': '1706',
        # 'EIA1280x720p@59.94': '1707',
        # 'EIA1280x720p@60': '1708',
        # 'EIA1280x720p@100': '1709',
        # 'EIA1280x720p@119.88': '1710',
        # 'EIA1280x720p@120': '1711',
        'EIA1920x1080p@23.98': '1712',
        # 'EIA1920x1080p@24': '1713',
        # 'EIA1920x1080p@25': '1714',
        # 'EIA1920x1080p@29.97': '1715',
        # 'EIA1920x1080p@30': '1716',
        # 'EIA1920x1080p@50': '1717',
        # 'EIA1920x1080p@59.94': '1718',
        # 'EIA1920x1080p@60': '1719',
        # 'EIA1920x1080p@100': '1720',
        'EIA1920x1080p@119.88': '1721',
        # 'EIA1920x1080p@120': '1722',
        'EIA1680x720p@23.98': '1723',
        'EIA1680x720p@24': '1724',
        'EIA1680x720p@25': '1725',
        'EIA1680x720p@29.97': '1726',
        'EIA1680x720p@30': '1727',
        'EIA1680x720p@50': '1728',
        'EIA1680x720p@59.94': '1729',
        'EIA1680x720p@60': '1730',
        'EIA1680x720p@100': '1731',
        'EIA1680x720p@119.88': '1732',
        'EIA1680x720p@120': '1733',
        'EIA2560x1080p@23.98': '1734',
        'EIA2560x1080p@24': '1735',
        'EIA2560x1080p@25': '1736',
        'EIA2560x1080p@29.97': '1737',
        'EIA2560x1080p@30': '1738',
        'EIA2560x1080p@50': '1739',
        'EIA2560x1080p@59.94': '1740',
        'EIA2560x1080p@60': '1741',
        'EIA2560x1080p@100': '1742',
        'EIA2560x1080p@119.88': '1743',
        'EIA2560x1080p@120': '1744',
        'EIA3840x2160p@23.98': '1745',
        'EIA3840x2160p@24': '1746',
        'EIA3840x2160p@25': '1747',
        'EIA3840x2160p@29.97': '1748',
        'EIA3840x2160p@30': '1749',
        'EIA3840x2160p@50': '1750',
        'EIA3840x2160p@59.94': '1751',
        'EIA3840x2160p@60': '1752',
        'EIA4096x2160p@23.98': '1753',
        'EIA4096x2160p@24': '1754',
        'EIA4096x2160p@25': '1755',
        'EIA4096x2160p@29.97': '1756',
        'EIA4096x2160p@30': '1757',
        'EIA4096x2160p@50': '1758',
        'EIA4096x2160p@59.94': '1759',
        'EIA4096x2160p@60': '1760',
        # 'EIA3840x2160p@23.98': '1761',
        # 'EIA3840x2160p@24': '1762',
        # 'EIA3840x2160p@25': '1763',
        # 'EIA3840x2160p@29.97': '1764',
        # 'EIA3840x2160p@30': '1765',
        # 'EIA3840x2160p@50': '1766',
        # 'EIA3840x2160p@59.94': '1767',
        # 'EIA3840x2160p@60': '1768',
        'EIA3840p50-420/8': '1771',
        'EIA3840p59.94-420/8': '1772',
        'EIA3840p60-420/8': '1773',
        'EIA4096p50-420/8': '1774',
        'EIA4096p59.94-420/8': '1775',
        'EIA4096p60-420/8': '1776',
        # 'EIA3840p50-420/8': '1777',
        # 'EIA3840p59.94-420/8': '1778',
        # 'EIA3840p60-420/8': '1779',
        'EIA3840p50-420/10': '1781',
        'EIA3840p59.94-420/10': '1782',
        'EIA3840p60-420/10': '1783',
        'EIA4096p50-420/10': '1784',
        'EIA4096p59.94-420/10': '1785',
        'EIA4096p60-420/10': '1786',
        # 'EIA3840p50-420/10': '1787',
        # 'EIA3840p59.94-420/10': '1788',
        # 'EIA3840p60-420/10': '1789',
        'EIA3840p50-420/12': '1791',
        'EIA3840p59.94-420/12': '1792',
        'EIA3840p60-420/12': '1793',
        'EIA4096p50-420/12': '1794',
        'EIA4096p59.94-420/12': '1795',
        'EIA4096p60-420/12': '1796',
        # 'EIA3840p50-420/12': '1797',
        # 'EIA3840p59.94-420/12': '1798',
        # 'EIA3840p60-420/12': '1799',
        'EIA3840p23.98-YC10': '1801',
        'EIA3840p24-YC10': '1802',
        'EIA3840p25-YC10': '1803',
        'EIA3840p29.97-YC10': '1804',
        'EIA3840p30-YC10': '1805',
        'EIA3840p50-YC10': '1806',
        'EIA3840p59.94-YC10': '1807',
        'EIA3840p60-YC10': '1808',
        'EIA4096p23.98-YC10': '1809',
        'EIA4096p24-YC10': '1810',
        'EIA4096p25-YC10': '1811',
        'EIA4096p29.97-YC10': '1812',
        'EIA4096p30-YC10': '1813',
        'EIA4096p50-YC10': '1814',
        'EIA4096p59.94-YC10': '1815',
        'EIA4096p60-YC10': '1816',
        # 'EIA3840p23.98-YC10': '1817',
        # 'EIA3840p24-YC10': '1818',
        # 'EIA3840p25-YC10': '1819',
        # 'EIA3840p29.97-YC10': '1820',
        # 'EIA3840p30-YC10': '1821',
        # 'EIA3840p50-YC10': '1822',
        # 'EIA3840p59.94-YC10': '1823',
        # 'EIA3840p60-YC10': '1824',
        # 'EIA3840p23.98-YC12': '1826',
        # 'EIA3840p24-YC12': '1827',
        # 'EIA3840p25-YC12': '1828',
        # 'EIA3840p29.97-YC12': '1829',
        # 'EIA3840p30-YC12': '1830',
        # 'EIA3840p50-YC12': '1831',
        # 'EIA3840p59.94-YC12': '1832',
        'EIA3840p60-YC12': '1833',
        'EIA4096p23.98-YC12': '1834',
        'EIA4096p24-YC12': '1835',
        'EIA4096p25-YC12': '1836',
        'EIA4096p29.97-YC12': '1837',
        'EIA4096p30-YC12': '1838',
        'EIA4096p50-YC12': '1839',
        'EIA4096p59.94-YC12': '1840',
        'EIA4096p60-YC12': '1841',
        'EIA3840p23.98-YC12': '1842',
        'EIA3840p24-YC12': '1843',
        'EIA3840p25-YC12': '1844',
        'EIA3840p29.97-YC12': '1845',
        'EIA3840p30-YC12': '1846',
        'EIA3840p50-YC12': '1847',
        'EIA3840p59.94-YC12': '1848',
        'HDTV1080': '1849',
        'HD 2048@23.98 YC422': '2001',
        '3G-B2048@23.98 YC444': '2002',
        '3G-B2048@23.98 RGB': '2003',
        'HD 2048@24 YC422': '2004',
        '3G-B2048@24 YC444': '2005',
        '3G-B2048@24 RGB': '2006',
        'HD 2048@25 YC422': '2007',
        '3G-B2048@25 YC444': '2008',
        '3G-B2048@25 RGB': '2009',
        'HD 2048@29.97 YC422': '2010',
        '3G-B2048@29.97 YC444': '2011',
        '3G-B2048@29.97 RGB': '2012',
        'HD 2048@30 YC422': '2013',
        '3G-B2048@30 YC444': '2014',
        '3G-B2048@30 RGB': '2015',
        '3G-B2048@47.95 YC422': '2016',
        '3G-B2048@47.95 YC444': '2017',
        '3G-B2048@47.95 RGB': '2018',
        '3G-B2048@48 YC422': '2019',
        '3G-B2048@48 YC444': '2020',
        '3G-B2048@48 RGB': '2021',
        '3G-B2048@50 YC422': '2022',
        '3G-B2048@50 YC444': '2023',
        '3G-B2048@50 RGB': '2024',
        '3G-B2048@59.94 YC422': '2025',
        '3G-B2048@59.94 YC444': '2026',
        '3G-B2048@59.94 RGB': '2027',
        '3G-B2048@60 YC422': '2028',
        '3G-B2048@60 YC444': '2029',
        '3G-B2048@60 RGB': '2030',
        '3G-B3840@23.98 RGB': '2031',
        'HD 3840@23.98 YC422': '2032',
        '3G-B3840@23.98 YC444': '2033',
        'HD 3840@24 YC422': '2034',
        '3G-B3840@24 YC444': '2035',
        '3G-B3840@24 RGB': '2036',
        'HD 3840@25 YC422': '2037',
        '3G-B3840@25 YC444': '2038',
        '3G-B3840@25 RGB': '2039',
        'HD 3840@29.97 YC422': '2040',
        '3G-B3840@29.97 YC444': '2041',
        '3G-B3840@29.97 RGB': '2042',
        'HD 3840@30 YC422': '2043',
        '3G-B3840@30 YC444': '2044',
        '3G-B3840@30 RGB': '2045',
        '3G-B3840@50 YC422': '2046',
        '3G-B3840@50 YC444': '2047',
        '3G-B3840@50 RGB': '2048',
        '3G-B3840@59.94 YC422': '2049',
        '3G-B3840@59.94 YC444': '2050',
        '3G-B3840@59.94 RGB': '2051',
        '3G-B3840@60 YC422': '2052',
        '3G-B3840@60 YC444': '2053',
        '3G-B3840@60 RGB': '2054',
        'HD 4096@23.98 YC422': '2055',
        '3G-B4096@23.98 YC444': '2056',
        '3G-B4096@23.98 RGB': '2057',
        'HD 4096@24 YC422': '2058',
        '3G-B4096@24 YC444': '2059',
        '3G-B4096@24 RGB': '2060',
        'HD 4096@25 YC422': '2061',
        '3G-B4096@25 YC444': '2062',
        '3G-B4096@25 RGB': '2063',
        'HD 4096@29.97 YC422': '2064',
        '3G-B4096@29.97 YC444': '2065',
        '3G-B4096@29.97 RGB': '2066',
        'HD 4096@30 YC422': '2067',
        '3G-B4096@30 YC444': '2068',
        '3G-B4096@30 RGB': '2069',
        '3G-B4096@47.95 YC422': '2070',
        '3G-B4096@47.95 YC444': '2071',
        '3G-B4096@47.95 RGB': '2072',
        '3G-B4096@48 YC422': '2073',
        '3G-B4096@48 YC444': '2074',
        '3G-B4096@48 RGB': '2075',
        '3G-B4096@50 YC422': '2076',
        '3G-B4096@50 YC444': '2077',
        '3G-B4096@50 RGB': '2078',
        '3G-B4096@59.94 YC422': '2079',
        '3G-B4096@59.94 YC444': '2080',
        '3G-B4096@59.94 RGB': '2081',
        '3G-B4096@60 YC422': '2082',
        '3G-B4096@60 YC444': '2083',
        '3G-B4096@60 RGB': '2084',
        'HD 2048@23.98sfYC422': '2101',
        '3B 2048@23.98sfYC444': '2102',
        '3B 2048@23.98sf RGB': '2103',
        'HD 2048@24sfYC422': '2104',
        '3B 2048@24sfYC444': '2105',
        '3B 2048@24sfRGB': '2106',
        'HD 2048@25sfYC422': '2107',
        '3B 2048@25sfYC444': '2108',
        '3B 2048@25sf RGB': '2109',
        'HD 2048@29.97sfYC422': '2110',
        '3B 2048@29.97sfYC444': '2111',
        '3B 2048@29.97sf RGB': '2112',
        'HD 2048@30sfYC422': '2113',
        '3B 2048@30sfYC444': '2114',
        '3B 2048@30sf RGB': '2115',
        '3B 3840@23.98sf RGB': '2116',
        'HD 3840@23.98sfYC422': '2117',
        '3B 3840@23.98sfYC444': '2118',
        'HD 3840@24sfYC422': '2119',
        '3B 3840@24sfYC444': '2120',
        '3B 3840@24sf RGB': '2121',
        'HD 3840@25sfYC422': '2122',
        '3B 3840@25sfYC444': '2123',
        '3B 3840@25sf RGB': '2124',
        'HD 3840@29.97sfYC422': '2125',
        '3B 3840@29.97sfYC444': '2126',
        '3B 3840@29.97sf RGB': '2127',
        'HD 3840@30sfYC422': '2128',
        '3B 3840@30sfYC444': '2129',
        '3B 3840@30sf RGB': '2130',
        'HD 4096@23.98sfYC422': '2131',
        '3B 4096@23.98sfYC444': '2132',
        '3B 4096@23.98sf RGB': '2133',
        'HD 4096@24sfYC422': '2134',
        '3B 4096@24sfYC444': '2135',
        '3B 4096@24sf RGB': '2136',
        'HD 4096@25sfYC422': '2137',
        '3B 4096@25sfYC444': '2138',
        '3B 4096@25sf RGB': '2139',
        'HD 4096@29.97sfYC422': '2140',
        '3B 4096@29.97sfYC444': '2141',
        '3B 4096@29.97sf RGB': '2142',
        'HD 4096@30sfYC422': '2143',
        '3B 4096@30sfYC444': '2144',
        '3B 4096@30sf RGB': '2145',
    }

    supported_video_patterns = {
        'Color Bar 100/100-H': '1001',
        'Color Bar SMPTE': '1004',
        'Black': '1125',
        'White': '1121',
        'R': '1122',
        'G': '1123',
        'B': '1124',
        'Magenta': '1127',
        'Cyan': '1128',
        'Yellow': '1129',
        'Monoscope': '1113',
        'Checker 1x1': '1201',
        'Checker 4x4': '1204',
        'Checker 8x8': '1205',
        'Cross Hatch': '1241',
    }

    supported_video_color_spaces = {
        'RGB': '0',
        'YCbCr444': '1',
        'YCbCr422': '2',
        '444': '1',
        '422': '2',
        'YCbCr420': '3',
    }
    # Note Infoframe maps colors to numbers differently from ASTRO numbers:
    # 'YCbCr422' : '1', 'YCbCr444' : '2',

    supported_video_color_depths = {
        '8-bit': '1',
        '10-bit': '2',
        '12-bit': '3',
    }

    supported_audio_sources = {
        'OFF': '0',
        'Ext.OPTICAL': '1',
        'Ext.COAXIAL': '2',
        'Ext.Analog PCM': '3',
        'Internal PCM': '4',
        'Ext.Analog DSD': '5',
        'Internal DSD': '6',
        'Internal IEC': '7',
        'Ext.I2S Non L-PCM': '8',
        'Ext.I2S L-PCM': '9',
        'Int.L-PCM': '10',
    }

    supported_audio_coding_types = {
        "Refer StreamHeader": "0",
        "IEC60958 PCM": "1",
        "AC-3": "2",
        "MPEG1": "3",
        "MP3": "4",
        "MPEG2": "5",
        "AAC": "6",
        "DTS": "7",
        "ATRAC": "8",
        "One Bit Audio": "9",
        "Dolby Digital +": "A",
        "DTS-HD": "B",
        "MLP": "C",
        "DST": "D",
        "WMA Pro": "E",
        "Refer Extension": "F"
    }

    supported_audio_coding_ext_type = {
        "HE-AAC": "3",
        "HE-AACv2": "4",
        "AAC LC": "5",
        "DRA": "6",
        "DTS": "7",
        "HE-AAC Surround": "8",
        "AAC-LC Surround": "9",
    }

    supported_audio_sample_rates = {
        'Mute': None,
        '32 KHz': '2',
        '44.1 KHz': '1',
        '48 KHz': '0',
        '88.2 KHz': '3',
        '96 KHz': '4',
        '176.4 KHz': '5',
        '192 KHz': '6',
        '352.8 KHz': '7',
        '384 KHz': '8',
        '705.6 KHz': '9',
        '768 KHz': '10',
    }

    supported_audio_sample_sizes = {
        '16-bit': '0',
        '20-bit': '1',
        '24-bit': '2',
    }

    supported_colorimetry = {
        'No Data': '0',
        'SMPTE170M/ITU601': '1',
        'ITU709': '2',
        'Extend': '3',
    }

    # Page 95
    supported_ext_color = {
        'xvYCC601': '0',
        'xvYCC709': '1',
        'sYCC601': '2',
        'AdobeYCC601': '3',
        'AdobeRGB': '4',
        'ITU-BT2020YCC': '5',
        'ITU-BT2020YCC-OR-RGB': '6',
    }

    supported_avi_ycc_range = {
        'Limited Range': '0',
        'Full Range': '1',
    }

    supported_avi_range = {
        'Default': '0',
        'Limited Range': '1',
        'Full Range': '2',
    }

    supported_audio_channel_counts = {
        'Refer StreamHeader': "0",
        '2ch': "1",
        '3ch': "2",
        '4ch': "3",
        '5ch': "4",
        '6ch': "5",
        '7ch': "6",
        '8ch': "7",
    }

    supported_audio_channel_speaker_placements = {
        '***-***-**-**-**-***-FR-FL': "0",
        '***-***-**-**-**-LFE-FR-FL': "1",
        '***-***-**-**-FC-***-FR-FL': "2",
        '***-***-**-**-FC-LFE-FR-FL': "3",
        '***-***-**-RC-**-***-FR-FL': "4",
        '***-***-**-RC-**-LFE-FR-FL': "5",
        '***-***-**-RC-FC-***-FR-FL': "6",
        '***-***-**-RC-FC-LFE-FR-FL': "7",
        '***-***-RR-RL-**-***-FR-FL': "8",
        '***-***-RR-RL-**-LFE-FR-FL': "9",
        '***-***-RR-RL-FC-***-FR-FL': "10",
        '***-***-RR-RL-FC-LFE-FR-FL': "11",
        '***-RC--RR-RL-**-***-FR-FL': "12",
        '***-RC--RR-RL-**-LFE-FR-FL': "13",
        '***-RC--RR-RL-FC-***-FR-FL': "14",
        '***-RC--RR-RL-FC-LFE-FR-FL': "15",
        'RRC-RLC-RR-RL-**-***-FR-FL': "16",
        'RRC-RLC-RR-RL-**-LFE-FR-FL': "17",
        'RRC-RLC-RR-RL-FC-***-FR-FL': "18",
        'RRC-RLC-RR-RL-FC-LFE-FR-FL': "19",
        'FRC-FLC-**-**-**-***-FR-FL': "20",
        'FRC-FLC-**-**-**-LFE-FR-FL': "21",
        'FRC-FLC-**-**-FC-***-FR-FL': "22",
        'FRC-FLC-**-**-FC-LFE-FR-FL': "23",
        'FRC-FLC-**-RC-**-***-FR-FL': "24",
        'FRC-FLC-**-RC-**-LFE-FR-FL': "25",
        'FRC-FLC-**-RC-FC-***-FR-FL': "26",
        'FRC-FLC-**-RC-FC-LFE-FR-FL': "27",
        'FRC-FLC-RR-RL-**-***-FR-FL': "28",
        'FRC-FLC-RR-RL-**-LFE-FR-FL': "29",
        'FRC-FLC-RR-RL-FC-***-FR-FL': "30",
        'FRC-FLC-RR-RL-FC-LFE-FR-FL': "31",
        '***-FCH-RR-RL-FC-***-FR-FL': "32",
        '***-FCH-RR-RL-FC-LFE-FR-FL': "33",
        'TC--***-RR-RL-FC-***-FR-FL': "34",
        'TC--***-RR-RL-FC-LFE-FR-FL': "35",
        'FRH-RLH-RR-RL-**-***-FR-FL': "36",
        'FRH-RLH-RR-RL-**-LFE-FR-FL': "37",
        'FRW-FLW-RR-RL-**-***-FR-FL': "38",
        'FRW-FLW-RR-RL-**-LFE-FR-FL': "39",
        'TC--RC--RR-RL-FC-***-FR-FL': "40",
        'TC--RC--RR-RL-FC-LFE-FR-FL': "41",
        'FCH-RC--RR-RL-FC-***-FR-FL': "42",
        'FCH-RC--RR-RL-FC-LFE-FR-FL': "43",
        'TC--FCH-RR-RL-FC-***-FR-FL': "44",
        'TC--FCH-RR-RL-FC-LFE-FR-FL': "45",
        'FRH-FLH-RR-RL-FC-***-FR-FL': "46",
        'FRH-FLH-RR-RL-FC-LFE-FR-FL': "47",
        'FRW-FLW-RR-RL-FC-***-FR-FL': "48",
        'FRW-FLW-RR-RL-FC-LFE-FR-FL': "49",
    }

    # Composite names to make handle odd file-based High Bit Rate audio testing
    supported_composite_audio_formats = {
        'Dolby_TrueHD_48KHz_5.1': ('22', '48 KHz', 0x1F),
        'Dolby_TrueHD_48KHz_6.1': ('23', '48 KHz', 0x3F),
        'Dolby_TrueHD_48KHz_7.1': ('24', '48 KHz', 0x7F),
        'Dolby_TrueHD_96KHz_5.1': ('26', '96 KHz', 0x1F),
        'Dolby_TrueHD_96KHz_6.1': ('27', '96 KHz', 0x3F),
        'Dolby_TrueHD_96KHz_7.1': ('28', '96 KHz', 0x7F),
        'Dolby_TrueHD_192KHz_5.1': ('30', '192 KHz', 0x1F),
        'DTS-HD_Master_48KHz_5.1': ('71', '48 KHz', 0x1F),
        'DTS-HD_Master_48KHz_6.1': ('72', '48 KHz', 0x3F),
        'DTS-HD_Master_48KHz_7.1': ('73', '48 KHz', 0x7F),
        'DTS-HD_Master_48KHz_7.1_ss': ('74', '48 KHz', 0x7F),
        'DTS-HD_Master_96KHz_5.1': ('75', '96 KHz', 0x1F),
        'DTS-HD_Master_96KHz_6.1': ('76', '96 KHz', 0x3F),
        'DTS-HD_Master_96KHz_7.1': ('77', '96 KHz', 0x7F),
        'DTS-HD_Master_96KHz_7.1_ss': ('78', '96 KHz', 0x7F),
        'DTS-HD_Master_192KHz_2': ('79', '192 KHz', 0x03),
        'DTS-HD_Master_192KHz_5.1': ('80', '192 KHz', 0x1F),
    }

    SUPPORTED_3D_EXTENSIONS = {
        "HHOO": "0",  # HorSubSampling(O/L,O/R)
        "HHOE": "1",  # HorSubSampling(O/L,E/R)
        "HHEO": "2",  # HorSubSampling(E/L,O/R)
        "HHEE": "3",  # HorSubSampling(E/L,E/R)
        "HQOO": "4",  # QuincunxMatrix(O/L,O/R)
        "HQOE": "5",  # QuincunxMatrix(O/L,E/R)
        "HQEO": "6",  # QuincunxMatrix(E/L,O/R)
        "HQEE": "7",  # QuincunxMatrix(E/L,E/R)
    }

    __video_format_short_names = {
        'EIA640x480p@59.94': 'VGAp@59',
        'EIA640x480p@60': 'VGAp@60',
        'EIA1440x480i@59.94': 'NTSCx2@59',
        'EIA1440x480i@60': 'NTSCx2@60',
        'EIA2880x480i@59.94': 'NTSCx4@59',
        'EIA2880x480i@60': 'NTSCx4@60',
        'EIA1440x576i@50': 'PALx2@50',
        'EIA2880x576i@50': 'PALx4@50',
        'EIA1280x720p@59.94': '720p59',
        'EIA1280x720p@60': '720p60',
        'EIA1920x1080i@59.94': '1080i59',
        'EIA1920x1080i@60': '1080i60',
        'EIA1920x1080p59.94': '1080p59',
        'EIA1920x1080p60': '1080p60',
        'EIA1920x1080p@23.97': '1080p23',
        'EIA1920x1080p@24': '1080p24',
        'EIA1920x1080p@29.97': '1080p29',
        'EIA1920x1080p@30': '1080p60',
    }

    __video_encodings_short_names = {
        'RGB': 'RGB',
        'YCbCr444': 'YCbCr444',
        'YCbCr422': 'YCbCr422',
        '444': 'YCbCr444',
        '422': 'YCbCr422',
        'YCbCr420': 'YCbCr420'
    }

    # Symbolic name for working ram
    __Buffer_RAM = '0'

    # Section 2.1; Page 17
    __LHT4_H_Timing_Record_Names = \
        ['us_Per_dot', 'Repetition',
         'DOT_CLOCK', 'H_PERIOD', 'H_DISPLAY',
         'H_SYNC', 'H_BACK_PORCH', 'HD_START', 'HD_WIDTH'
        ]

    # Section 2.3; Page 19
    __LVT4_V_Timing_Record_Names = \
        ['SCAN_MODE', 'SERRATION', 'ENQ_On_Off',
         'V_TOTAL', 'V_SYNC',
         'ENQ_FP', 'ENQ_BP',
         'V_BACK_PORCH', 'V_DISPLAY', 'VD_START', 'VD_WIDTH',
         'V_TOTAL2', 'V_SYNC2', 'END_FP2', 'ENQ_BP2',
         'V_BACK_PORCH2', 'V_DISPLAY2', 'VD_START2', 'VD_WIDTH2',
         'Tv_Mode', 'Reserved_32'
        ]

    # Section 2.5; Page 23
    __LOT4_Output_Condition_Record_Names = \
        ['YPbPr', 'YPbPr_No',
         'Color_Diff_YR', 'Color_Diff_YG', 'Color_Diff_YB',
         'Color_Diff_CbR', 'Color_Diff_CbG', 'Color_Diff_CbB',
         'Color_Diff_CrR', 'Color_Diff_CrG', 'Color_Diff_C4B',
         'HS_On_Off', 'HS_Mode', 'HS_Sel',
         'VS_On_Off', 'VS_Mode',
         'CS_On_Off', 'CS_Mode', 'CS_Sel',
         'CV_On_Off', 'CV_Mode',
         'Analog_Video_Level', 'Analog_Setup_Level', 'Analog_Sync_Level',
         'Output_Bit_Len', 'HDCP_Disp_Port',
         'D_Connector_Line1', 'D_Connector_Line2', 'D_Connector_Line3',
         'Reserved',
         'PC_BNC_On_Off', 'PC_BNC_DSUB_On_Off',
         'VBS_On_Off', 'BNC_On_Off',
         'S_Connector_On_Off', 'D_Connector_On_Off', 'TV_DSUB_On_Off',
         'SCART1_On_Off', 'SCART2_On_Off',
         'HDMI1_On_Off', 'HDMI2_On_Off',
         'DVI_D1_On_Off', 'DVI_D2_On_Off',
         'LVDS_D1_On_Off', 'LVDS_D2_On_Off', 'LVDS_D3_On_Off', 'LVDS_D4_On_Off',
         'PARA1_On_Off', 'PARA2_On_Off', 'PARA3_On_Off', 'PARA4_On_Off',
         'S_Connector',
         'DVI_Dual_Line_Mode', 'DVI_Ctl0', 'DVI_Ctl1',
         'Aspect_Mode', 'Aspect_H', 'Aspect_V',
         'HDCP_Enable',
         'Level_Mode1', 'Level_Mode2', 'Level_Mode3', 'Level_Mode4',
         'Level_Mode5', 'Level_Mode6', 'Level_Mode7', 'Level_Mode8',
         'Level_Mode9', 'Level_Mode10', 'Level_Mode11', 'Level_Mode12',
         'Level_Mode13', 'Level_Mode14', 'Level_Mode15', 'Level_Mode16',
         'Signal_Name_Disp_On',
         'DisplayPort1_On_Off', 'DisplayPort2_On_Off'
                                'TV_DVI_Digital_On_Off',
         'TMDS1_On_Off', 'TMDS2_On_Off',
         # BUG get info about contents
         'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11',
        ]

    # Section 2.21; Page 70
    # Source is 4 for internal PCM,
    # 6 for DSD (programs 91 .. 95)
    # 7 for IEC (1, 2, 11, 12, 13, 14, 22, 23, 24, 26, 27, 28, 30,
    # 41, 42, 51, 52, 53, 56, 57, 58, 61, 62, 63, 64, 65,
    # 66, 67, 68, 72, 73, 74, 74, 75, 76, 77, 78, 80, 86, 87)
    # NOTE for DSD, must set InfoFrame to channel count,
    # sample frequency, speaker placement
    __LDAD4_Audio_Digital_Record_Names = \
        ['Sample', 'Source', 'Width', 'Level_Mode',
         'Level_1', 'Level_2', 'Level_3', 'Level_4',
         'Level_5', 'Level_6', 'Level_7', 'Level_8',
         'Freq_1', 'Freq_2', 'Freq_3', 'Freq_4',
         'Freq_5', 'Freq_6', 'Freq_7', 'Freq_8',
         'Data_1', 'Data_2', 'Data_3', 'Data_4',
         'Data_5', 'Data_6', 'Data_7', 'Data_8',
         'LPCM',
        ]

    # Section 2.23
    __LHDMI4_HDMI_Record_Names = \
        ['HDMI_Mode',  # 4: Auto
         'Video_Format',  # 0: RGB, 1: YCbCr444, 2: YCbCr422
         'Audio_Out',  # 1: On
         'Video_Width',  # 0: Auto, 1: 8-bit, 2: 10-bit, 3: 12-bit
        ]

    # Section 2.25
    __LIF4_InfoFrame_Record_Names = \
        ['AVI_On', 'SPD_On', 'Audio_On', 'MPEG_On',
         'AVI_Type', 'AVI_Ver', 'AVI_Scan_Info', 'ABI_Bar_Info',
         'AVI_Active_Format',
         'AVI_RGB_YCbCr', 'AVI_Active_Frame_Aspect', 'AVI_Picture_Aspect',
         'AVI_Colorimetry', 'AVI_Video_Code', 'AVI_Repetition',
         'AVI_TopBar', 'AVI_BottomBar', 'AVI_L_Bar', 'AVI_R_Bar',
         'AVI_Scaling', 'AVI_QuantRange', 'AVI_ExtColor', 'AVI_IT_Content',
         'SPD_Type', 'SPD_Ver',
         'SPD_Vendor_Name_8',
         'SPD_Product_20',
         'SPD_Source_Device',
         'Audio_Type', 'Audio_Ver',
         'Audio_Channel_Count', 'Audio_Coding_Type',
         'Audio_Sample_Size', 'Audio_Sample_Freq',
         'Audio_Channel_Alloc', 'Audio_Level_Shift',
         'Audio_Down_Mix',
         'MPEG_Type', 'MPEG_Ver', 'MPEG_Frame', 'MPEG_Field_Repeat',
         'MPEG_Bit_Rate',
         'AVI_IT_Content_Type', 'AVI_YCC_Quantization_Range',
         'Audio_LFE_Playback_Level', 'Audio_Coding_Type_Extension',
         'Chk_Sum_Mode',  # 0: automatic
         'Chk_Sum', 'Info_Len', 'Data_Byte_14', 'Data_Byte_15',
        ]

    # Section 2.92
    __LVIF4_Vendor_Specific_InfoFrame_Data_Names = [
        "On/Off", "Type", "Version", "IEEE ID", "Payload Length",
        "Payload 1", "Payload 2", "Payload 3", "Payload 4", "Payload 5",
        "Payload 6", "Payload 7", "Payload 8", "Payload 9", "Payload 10",
        "Payload 11", "Payload 12", "Payload 13", "Payload 14", "Payload 15",
        "Payload 16", "Payload 17", "Payload 18", "Payload 19", "Payload 20",
        "Payload 21", "Payload 22", "Payload 23",
        "Rsv", "HDMI Video Format", "HDMI VIC",
        "3D Structure", "3D Extension", "3D Meta Present", "3D Meta Type", "3D Meta Data Length",
        "3D Meta Data 1", "3D Meta Data 2", "3D Meta Data 3", "3D Meta Data 4", "3D Meta Data 5",
        "3D Meta Data 6", "3D Meta Data 7", "3D Meta Data 8", "3D Meta Data 9", "3D Meta Data 10",
        "3D Meta Data 11", "3D Meta Data 12", "3D Meta Data 13", "3D Meta Data 14", "3D Meta Data 15",
        "3D Meta Data 16", "3D Meta Data 17", "3D Meta Data 18", "3D Meta Data 19",
        "VendorSpec I/F Type", "3D Meta Data 20", "3D Meta Data 21",
        "Version 1", "3D Valid", "3D Additional Info Present", "3D Dual View", "3D View Dependency",
        "3D Preferred 2D View", "3D Disparity Data Present", "3D Disparity Data Ver", "3D Disparity Data Length",
        "3D Disparity Data 1", "3D Disparity Data 2", "3D Disparity Data 3", "3D Disparity Data 4",
        "3D Disparity Data 5", "3D Disparity Data 6", "3D Disparity Data 7", "3D Disparity Data 8",
        "3D Disparity Data 9", "3D Disparity Data 10", "3D Disparity Data 11", "3D Disparity Data 12",
        "3D Disparity Data 13", "3D Disparity Data 14", "3D Disparity Data 15", "3D Disparity Data 16",
        "3D Disparity Data 17", "3D Disparity Data 18", "3D Disparity Data 19", "3D Disparity Data 20",
        "3D Disparity Data 21", "3D Disparity Data 22", "3D Disparity Data 23", "3D Disparity Data 24",
        "3D Disparity Data 25", "3D Disparity Data 26", "3D Disparity Data 27", "3D Disparity Data 28",
        "3D Disparity Data 29", "3D Disparity Data 30", "3D Disparity Data 31",
    ]

    __L3DIMG4_3D_Image_Record_Names = [
        "program_no", "image_type", "left_image", "right_image", "left_deviation", "right_deviation",
        "lr_on/off", "color_r", "color_g", "color_b", "level_l", "level_r", "output_mode",
        "lr_display", "lr_black_back", "sub_sampling"
    ]

    # Section 2.43
    __PNAMER4_Program_Name_Record_Names = \
        ['Length',
         'String_20',
        ]

    # Private conversation with Astro
    __LINFO_MAC_Address_Record_Names = ['Address']

    __LINFO_License_Record_Names = \
        ['License_Code_1', 'License_Info_1',  # Repeated field
         'License_Code_2', 'License_Info_2',  # Repeated field
         'License_Code_3', 'License_Info_3',  # Repeated field
         'License_Code_4', 'License_Info_4',  # Repeated field
         'License_Code_5', 'License_Info_5',  # Repeated field
         'License_Code_6', 'License_Info_6',  # Repeated field
         'License_Code_7', 'License_Info_7',  # Repeated field
         'License_Code_8', 'License_Info_8',  # Repeated field
        ]

    __LINFO_Engine_Board_Record_Names = \
        ['Board_Serial_Number',
         'Board_Version',
         'Custom_Order_ID',
         'Custom_Order_Revision',
         'Engine_Main_FPGA_Version',
         'Engine_Sub_FPGA_Version',
         'Engine_Rear_FPGA_Version',
         'VG_Type',
         'Custom_Order_Type',
         'CPU_ROM_Version',
         'Custom_Order_ROM_Version',
         'VG_Serial_Number',
        ]

    __LINFO_Slot_012M_Record_Names = \
        ['Serial_No',
         'Board_Type',
         'Board_Version',
         'Custom_Order_Type',
         'Custom_Order_Version',
         'FPGA_Version',
         'Firmware_Version',
        ]

    # Transmission Control characters:
    __ENQ = '\x05'  # Request to start Teminal Mode
    __EOT = '\x04'  # Request to end Teminal Mode
    __ACK = '\x06'  # Positive Acknowledgement
    __NAK = '\x15'  # Negative Acknowledgement
    __STX = '\x02'  # Start of text (command)
    __ETB = '\x17'  # End of text (data)
    __ETX = '\x03'  # End of text (command, data)
    __TRDT = '\x10'  # Marks beginning of block of data
    __ESTS = '\x11'  # Marks beginning of error notification
    __EXTCMD = '\xFF'  # Extended command identification code
    __VG4CMD = '\xFD'  # New command identification code
    __COMMA_DELIM = '\x2C'  # normal delimiter ','
    __SEMI_DELIM = '\x3B'  # alternate delimiter ';', used in SPD4 (Section 2.13; page 88)

    # Transmission Control Characters
    __Transmission_Ctl_Chars = {
        ord(__ENQ): '<ENQ>',
        ord(__EOT): '<EOT>',
        ord(__ACK): '<ACK>',
        ord(__NAK): '<NAK>',
        ord(__STX): '<STX>',
        ord(__ETB): '<ETB>',
        ord(__ETX): '<ETX>',
        ord(__TRDT): '<TRDT>',
        ord(__ESTS): '<ESTS>',
        ord(__EXTCMD): '<EXTCMD>',
        ord(__VG4CMD): '<VG4CMD>',
        ord(__COMMA_DELIM): ',',
        ord(__SEMI_DELIM): ';',
    }

    # Command names used by the Astro box
    __SDAD4 = '\x20\x34'  # Set audio data digital; Section 2.21; Page 70
    __LDAD4 = '\x20\x35'  # Load audio data digital; Section 2.22; Page 72

    __LIDNO4 = '\x20\x83'  # Load serial number; Section 2.97; Page 172;
    __EXPDN4 = '\x24\x20'  # Execute program; Section 2.104; Page 181
    __EXBN4 = '\x24\x22'  # Execute Buffer Ram program; Section 2.106; Page 183

    __SHT4 = '\x20\x20'  # Set H timing; Section 2.1; page 17
    __LHT4 = '\x20\x21'  # Load H timing; Section 2.2; page 18

    __SVT4 = '\x20\x22'  # Set V timing; Section 2.3; page 19
    __LVT4 = '\x20\x23'  # Load V timing; Section 2.4; page 21

    __SOT4 = '\x20\x24'  # Set Output Condition register; Section 2.5; page 23
    __LOT4 = '\x20\x25'  # Load Output Condition register; Section 2.6; page 27

    __SPTS4 = '\x20\x2A'  # Set Pattern Select data; Section 2.11; page 37
    __LPTS4 = '\x20\x2B'  # Load Pattern Select data; Section 2.12; page 39

    __SHDMI4 = '\x20\x36'  # Set hdmi info; Section 2.23; page 74
    __LHDMI4 = '\x20\x37'  # Set hdmi info; Section 2.24; page 75

    __SIF4 = '\x20\x38'  # Set Info Frame info; Section 2.25; page 76
    __LIF4 = '\x20\x39'  # Load Info Frame info; Section 2.26; page 79

    __SPD4 = '\x20\x3E'  # Set Program Data; Section 2.31; page 88
    __LPD4 = '\x20\x3F'  # Load Program Data; Section 2.32; page 90 prog, len, 20 bytes

    __PNAMES4 = '\x20\x4A'  # Register Program Name; Section 2.42; page 103

    __HDCPON4 = '\x24\x28'  # HDCP enable; Section 2.112; page 190
    __PBPRON4 = '\x24\x29'  # Instant switch to color difference; Section 2.113; page 191

    __LEDID4 = '\x24\x2B'  # read EDID; Section 2.115; page 193

    __EXPONOFF4 = '\x24\x30'  # Pattern info on/off Section BUG
    __LHDCP4 = '\x24\x3D'  # Load state of HDCP; Section 2.126; Page 209
    __MUTEON4 = '\x24\x3E'  # Set Mute; Section 2.127; Page 210
    __LGROUP4 = '\x20\x53'  # Group data readout; Section 2.49; Page 110
    __LOPTB = '\x74'  # Optional board data acquisition; Section 4.69; Page 326

    __LVIF4 = '\x20\x7F'  # 2.93 LVIF4 [20H 7FH]: Vendor Specific InfoFrame data acquisition
    __SVIF4 = '\x20\x7E'  # 2.92 SVIF4 [20H 7EH]: Vendor Specific InfoFrame data setting

    __S3DIMG4 = '\x20\xB5'  # 2.130 S3DIMG4［20H B5H］ :3D Image pattern data setting
    __L3DIMG4 = '\x20\xB5'  # 2.131 L3DIMG4 [20H B5H] :3D Image pattern data aquisition

    __LINFO4 = '\x20\x96'  # Undocumented command to get info

    # HMM.  Chapter 4 has single-byte commands.  No more fancy *4 commands

    def __init__(self, host=None, port=8000):
        self.__host = None
        self.__port = None
        self.__sock = None

        self.__video_hdcp_enabled = True
        self.__video_program = 'EIA1280x720p@60'
        self.__video_color_space = 'RGB'
        self.__video_color_depth = '8-bit'
        self.__video_pattern = 'Color Bar SMPTE'
        self.__video_mute = False

        self.__audio_source = 'Internal PCM'
        self.__audio_file = '1'
        self.__audio_channel_speaker_placement = 0x03
        self.__audio_channel_count = '2ch'
        self.__audio_sample_rate = '44.1 KHz'
        self.__audio_sample_size = '16-bit'
        self.__audio_mute = False

        self.__video_3d_extension = None

        self.__avi_range = None
        self.__avi_ycc_range = None
        self.__ext_colorimetry = None
        self.__basic_colorimetry = None

        if host is not None:
            self.connect(host, port)

    def connect(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.connect((self.__host, self.__port))
        self.__init_state()

    def close(self):
        if self.__sock is not None:
            self.__sock.close()
            self.__sock = None

    def __init_state(self):
        self.video_mute_immediate(False)
        self.audio_mute_immediate(False)

    def __send(self, data):
        logger.debug("send: %r", self.__class__.format_message(data))
        # data = data.encode("latin-1")
        self.__sock.send(data)

    def __recv(self, size):
        data = self.__sock.recv(size)
        # data = data.decode()
        logger.debug("recv: %r", self.__class__.format_message(data))
        return data

    def load(self, video_program, video_pattern, video_color_space, video_color_depth,
             audio_channel_count, audio_sample_rate, audio_sample_size,
             audio_source="Internal PCM", audio_file="1", audio_channel_speaker_placement=None,
             video_3d_extension=None):
        logger.debug('Setting video format to: %s, %s, %s, %s', video_program, video_pattern, video_color_space,
                     video_color_depth)
        logger.debug('Setting audio format to: %s, %s, %s', audio_channel_count, audio_sample_rate, audio_sample_size)
        self.__video_program = video_program
        self.__video_pattern = video_pattern
        self.__video_color_space = video_color_space
        self.__video_color_depth = video_color_depth
        self.__audio_channel_count = audio_channel_count
        self.__audio_sample_rate = audio_sample_rate
        self.__audio_sample_size = audio_sample_size
        self.__audio_source = audio_source
        self.__audio_file = audio_file
        self.__audio_channel_speaker_placement = audio_channel_speaker_placement or 2 ** int(
            audio_channel_count[0]) - 1 if audio_channel_count[0].isdigit() else 0x03
        self.__video_3d_extension = video_3d_extension
        if video_3d_extension is not None and "Side_half" not in video_program:
            raise ValueError("video_3d_extension can only be set when 3D structure is Side_half")
        self.execute()

    def set_csc_params(self, basic_color="ITU709", ext_color="xvYCC709", avi_range="Full Range",
                       avi_ycc_range="Full Range"):
        """
        info_frame['AVI_Colorimetry'] = self.supported_colorimetry[self.__basic_colorimetry]
        info_frame['AVI_ExtColor'] = self.supported_ext_color[self.__ext_colorimetry]
        info_frame['AVI_QuantRange'] = self.supported_avi_range[self.__avi_range]
        info_frame['AVI_YCC_Quantization_Range'] = self.supported_avi_ycc_range[self.__avi_ycc_range]
        """
        self.__basic_colorimetry = basic_color
        self.__ext_colorimetry = ext_color
        self.__avi_range = avi_range
        self.__avi_ycc_range = avi_ycc_range

    def load_video(self, program, pattern, color_space, color_depth, video_3d_extension=None):
        logger.debug('Setting video format to: %s, %s, %s, %s', program, pattern, color_space, color_depth)
        self.__video_program = program
        self.__video_pattern = pattern
        self.__video_color_space = color_space
        self.__video_color_depth = color_depth
        self.__video_3d_extension = video_3d_extension
        if video_3d_extension is not None and "Side_half" not in program:
            raise ValueError("video_3d_extension can only be set when 3D structure is Side_half")
        self.execute()

    def load_audio(self, channel_count, sample_rate, sample_size,
                   source="Internal PCM", fileid="1", channel_speaker_placement=None):
        logger.debug('Setting audio format to: %s, %s, %s', channel_count, sample_rate, sample_size)
        self.__audio_channel_count = channel_count
        self.__audio_sample_rate = sample_rate
        self.__audio_sample_size = sample_size
        self.__audio_source = source
        self.__audio_file = fileid
        self.__audio_channel_speaker_placement = channel_speaker_placement or 2 ** int(channel_count[0]) - 1 if \
            channel_count[0].isdigit() else 0x03
        self.execute()

    def load_composite_audio_format(self, audio_format):
        audio_format_info = self.supported_composite_audio_formats[audio_format]
        self.__audio_source = 'Internal IEC'
        self.__audio_sample_rate = audio_format_info[1]
        self.__audio_sample_size = '24-bit'
        self.__audio_channel_speaker_placement = audio_format_info[2]
        self.__audio_channel_count = "Refer StreamHeader"
        self.__audio_file = audio_format_info[0]

    def load_composite_video_format(self, video_format):
        self.__video_pattern = 'Color Bar 100/100-H'
        video_format_info = video_format
        video_info_list = video_format_info.split("::")
        fake_program = video_info_list[0]
        video_timing = video_info_list[1]
        real_program = list()
        for k, v in self.supported_video_programs.items():
            if video_timing in k:
                real_program.append(k)
        assert len(real_program) == 1, "We can found more than one program from {%s} based on your input {%s}. " \
                                       "Please provide more explicit video format information!" % (
                                           self.supported_video_programs, video_format)
        self.__video_program = real_program[0]

    def execute(self):
        """
        Send all info to the Video Generator
        Seems to be done in several phases:
        1) Set Video format.  This sets horizontal and vertical timing
        2) Set color depth, color encoding
        3) Set up Audio info, including encoding and sample rate
        4) Set info frames to be consistent with data
        5) Create video pattern

        Here is what a user of the box does manually:
        A) Select a video program with desirable timing specs:
        B) Select Color Depth
           menu/config/set/general/set/color depth/8-10-12
        C) Set Color encoding
           menu/Program Edit/set/Output/digital output/hdmi/video format
           menu/Program Edit/set/Output/digital output/hdmi/info_frame/avi
           make the same.
        D) Pattern select.  1201 is 1-pixel checkers.  1000 is colorbars
        E) menu/program edit/audio/digital audio
           useful things are pcm, 44.1, 48, 96, 24 bit
        """

        # self.output_enable_immediate(False)
        self.__setup_video_program()
        self.__setup_video_pattern()
        self.__setup_audio()
        self.__setup_info_frame()
        if self.__video_3d_extension is not None:
            self.__setup_vendor_specific_infoframe()
        self.__setup_display_name()
        # self.output_enable_immediate(True)

    # External Interface
    def output_enable_immediate(self, output_en):
        """
        Disable HDMI potput (if possible)
        """
        logger.debug('vg_ASTRO_870 output_enable "%s"' % output_en)
        # LOT4 (0x20, 0x25); Type 3; Section 2.6; Page 27
        output_condition = self._type_3_read_block(self.__LOT4, params=[self.__Buffer_RAM])
        output_condition = output_condition.split(self.__COMMA_DELIM)
        output_condition = collections.OrderedDict(
            zip(self.__LOT4_Output_Condition_Record_Names, output_condition))
        if output_en:
            output_condition['HDMI1_On_Off'] = '1'
            output_condition['HDMI2_On_Off'] = '1'
        else:
            output_condition['HDMI1_On_Off'] = '0'
            output_condition['HDMI2_On_Off'] = '0'
        output_condition_list = output_condition.values()
        output_condition_list.insert(0, self.__Buffer_RAM)  # write back to program 0
        self._type_2_command(self.__SOT4, params=output_condition_list)
        self._type_2_command(self.__EXBN4)

    def hdcp_enable_immediate(self, hdcp_en):
        hdcp_char = '1' if hdcp_en else '0'
        self._type_2_command(self.__HDCPON4, params=[hdcp_char])

    def video_mute_immediate(self, video_mute):
        logger.debug('Setting video_mute to "%s"' % video_mute)
        self.__video_mute = video_mute

    def audio_mute_immediate(self, audio_mute):
        logger.debug('Setting audio_mute to "%s"' % audio_mute)
        mute_char = '1' if audio_mute else "0"
        self.__audio_mute = audio_mute
        self._type_2_command(self.__MUTEON4, params=[mute_char])

    @classmethod
    def format_message(cls, data):
        data_chars = ''
        for char in data:
            if ord(char) in cls.__Transmission_Ctl_Chars:
                c_repr = cls.__Transmission_Ctl_Chars[ord(char)]
            else:
                c_repr = char
            # elif (char in string.ascii_letters) or (char in string.digits):
            # c_repr = char
            # else:
            # c_repr = '<0x%x>' % ord(char)
            data_chars += c_repr
        return data_chars

    @classmethod
    def __display_message(cls, data):
        msg = cls.format_message(data)
        logger.debug(msg)

    def __do_peek(self, command):
        return self._type_3_read_block(command, params=[self.__Buffer_RAM])

    def __setup_video_program(self):
        """
        A Video Format defines frame rate, line width in pixels, screen height in lines
        In the Astro_870, invoke pre-defined programs with timing already set
        """
        # Program Data execute EXPDN4 (0x24 0x20); Type 2, Section 2.104; Page 181;
        # Params: Program Number, execution mode (0=program,
        # 1=timing, 2=pattern)
        # This moves timing info into the 'buffer ram', pattern 0

        program = self.supported_video_programs[self.__video_program]
        self._type_2_command(self.__EXPDN4, params=[program, '1'])

        # HDMI Data; SHDMI4 (0x20, 0x36); Type 2; Section 2.23; page 74
        # Params: program number
        # (??? 0: buffer ram, 1..999, 0000: command work ram)
        # HDMI Mode(0:off, 1:dvi, 2:hdmi 1.0, 3: hdmi 1.1, 4:auto),
        # Video Format(0 RGB, 1: YCbCr444, 2: YCbCr422),
        #            Audio Out (1 on),
        #            Video Width (0=auto, 1=8, 2=10, 3=12)
        #    Refer to __LHDMI4_HDMI_Record_Names
        # Set color depth to automatic, to track the SOT4 value
        # Set color encoding to correct value, used by SIF4
        # Set Audio Mute (not sure if needed)
        color_space = self.supported_video_color_spaces[self.__video_color_space]
        if self.__audio_mute:
            audio_enable = '0'
        else:
            audio_enable = '1'
        color_depth = self.supported_video_color_depths[self.__video_color_depth]

        self._type_2_command(self.__SHDMI4, params=[self.__Buffer_RAM, '4', color_space, audio_enable, color_depth])
        self._type_2_command(self.__EXBN4)

    def __setup_video_pattern(self):
        """
        A Video Pattern defines video content with possible text overlay
        In the Astro_870, invoke pre-defined programs with pattern already set
        TODO: Maybe make pattern in software, enable pattern overlay memory??
        """
        # Program Data execute EXPDN4 (0x24 0x20); Type 2, Section 2.104; Page 181;
        # Params: Program Number, execution mode (0=program,
        # 1=timing, 2=pattern)
        # This moves Video pattern info into the 'buffer ram', pattern 0
        program = self.supported_video_patterns[self.__video_pattern]
        self._type_2_command(self.__EXPDN4, params=[program, '2'])

    def __setup_audio(self):
        """
        Audio is parameterized by Sample Rate, Sample Size, Number of Channels,
          and content.
        """
        # Audio Data Digital: SDAD4 (0x20, 0x34); Type 2; Section 2.21; Page 70
        # Params: Program Number(1 to 4 digits), Audio Clock(1 byte),
        # Audio Source(4 internal PCM), Audio Width (0=16, 1=20, 2=24),
        # output level mode (0 db, 1 bit), 8 separate levels,
        # 8 internal frequencies, 8 audio data numbers (?),
        # one field of 8 characters (0 = off, 1 = on)
        # Maximum amplitude is 8388607.  20 db down is 1/10 == 838861
        # Should this value change when the number of bits change?
        audio_sample_rate = self.supported_audio_sample_rates[self.__audio_sample_rate]
        audio_size = self.supported_audio_sample_sizes[self.__audio_sample_size]

        audio_source = self.supported_audio_sources[self.__audio_source]
        audio_freq = '1000'

        audio_channels = self.__audio_channel_speaker_placement
        audio_file = self.__audio_file

        audio_mask = ''  # LSB becomes channel 8 info
        for i in range(8):
            if (audio_channels & 0x01) != 0:
                audio_mask += '1'  # shift left by extending
            else:
                audio_mask += '0'
            audio_channels >>= 1

        audio_ampl = '838861'

        self._type_2_command(
            self.__SDAD4,
            params=['0',
                    audio_sample_rate, audio_source, audio_size,
                    '0',  # db
                    audio_ampl, audio_ampl, audio_ampl, audio_ampl,
                    audio_ampl, audio_ampl, audio_ampl, audio_ampl,
                    audio_freq, audio_freq, audio_freq, audio_freq,
                    audio_freq, audio_freq, audio_freq, audio_freq,
                    audio_file, audio_file, audio_file, audio_file,
                    audio_file, audio_file, audio_file, audio_file,
                    audio_mask])
        print ['0',
                    audio_sample_rate, audio_source, audio_size,
                    '0',  # db
                    audio_ampl, audio_ampl, audio_ampl, audio_ampl,
                    audio_ampl, audio_ampl, audio_ampl, audio_ampl,
                    audio_freq, audio_freq, audio_freq, audio_freq,
                    audio_freq, audio_freq, audio_freq, audio_freq,
                    audio_file, audio_file, audio_file, audio_file,
                    audio_file, audio_file, audio_file, audio_file,
                    audio_mask]
        self._type_2_command(self.__EXBN4)

        output_condition = self._type_3_read_block(self.__LOT4, params=[self.__Buffer_RAM])
        output_condition = output_condition.split(self.__COMMA_DELIM)
        output_condition = collections.OrderedDict(zip(self.__LOT4_Output_Condition_Record_Names, output_condition))

        if self.__video_color_space == 'RGB':
            output_condition['YPbPr'] = '0'
        else:
            output_condition['YPbPr'] = '1'
        if self.__video_color_depth == '8-bit':
            output_condition['Output_Bit_Len'] = '8'
        elif self.__video_color_depth == '10-bit':
            output_condition['Output_Bit_Len'] = '10'
        else:
            output_condition['Output_Bit_Len'] = '12'
        if self.__video_hdcp_enabled:
            output_condition['HDCP_Enable'] = '1'
        else:
            output_condition['HDCP_Enable'] = '0'
        output_condition_list = list(output_condition.values())
        output_condition_list.insert(0, self.__Buffer_RAM)  # write back to program 0
        self._type_2_command(self.__SOT4, params=output_condition_list)
        self._type_2_command(self.__EXBN4)

    def __setup_vendor_specific_infoframe(self):
        extension = self.SUPPORTED_3D_EXTENSIONS[self.__video_3d_extension]

        info_frame = self._type_3_read_block(self.__LVIF4, params=[self.__Buffer_RAM])
        info_frame = info_frame.split(self.__COMMA_DELIM)
        info_frame = collections.OrderedDict(zip(self.__LVIF4_Vendor_Specific_InfoFrame_Data_Names, info_frame))

        info_frame["3D Extension"] = extension

        info_frame_list = list(info_frame.values())
        info_frame_list.insert(0, self.__Buffer_RAM)
        self._type_2_command(self.__SVIF4, params=info_frame_list)
        self._type_2_command(self.__EXBN4)

    def __setup_info_frame(self):
        # Read-Modify-Write InfoFrame info from program 0
        # Infoframe; SIF4 (0x20, 0x38); type 2; Section 2.25; page 76
        # Params: Program number, AVI On, SPD On, Audio ON, MPED On, AVI_type (2),
        # AVI Ver, AVI Scan Info, AVI Bar Info, AVI Active Format,
        # AVI RGB (0 RGB, 1: YCbCr422, 2: YCbCr444),
        # AVI Active Frame ASpect (0), AVI Picture Acpect (1:4:3, 2:16:9),
        # AVI Color (0 None, 1 SMPTE, 2 ITU709, 3 Extend),
        #            Lots of other stuff.
        # Two cases seen:  Char 0 is '1' for automatic,
        #                  Char 9 is '2' for 444, '1' for 422, '0' for RGB
        #                  Note that this is different than encoding info in LHDMI4
        info_frame = self._type_3_read_block(self.__LIF4, params=[self.__Buffer_RAM])
        info_frame = info_frame.split(self.__COMMA_DELIM)
        info_frame = collections.OrderedDict(zip(self.__LIF4_InfoFrame_Record_Names, info_frame))
        # Widen Text fields to their fixed-width values
        vendor_name = info_frame['SPD_Vendor_Name_8']
        info_frame['SPD_Vendor_Name_8'] = (vendor_name + '\x00' * 8)[0:8]
        # Widen Text fields to their fixed-width values
        product_name = info_frame['SPD_Product_20']
        info_frame['SPD_Product_20'] = (product_name + '\x00' * 16)[0:16]

        info_frame['AVI_On'] = '1'
        # Encoding different than in SHDMI4
        # BUG look up in color_encodings
        info_frame_color = self.supported_video_color_spaces[self.__video_color_space]
        if info_frame_color == '1':
            info_frame_color = '2'
        elif info_frame_color == '2':
            info_frame_color = '1'
        info_frame['AVI_RGB_YCbCr'] = info_frame_color
        info_frame['Audio_Channel_Count'] = self.supported_audio_channel_counts[self.__audio_channel_count]
        info_frame['Audio_Sample_Freq'] = self.supported_audio_sample_rates[self.__audio_sample_rate]
        info_frame['Audio_Sample_Size'] = self.supported_audio_sample_sizes[self.__audio_sample_size]
        try:
            info_frame['AVI_Colorimetry'] = self.supported_colorimetry[self.__basic_colorimetry]
            info_frame['AVI_ExtColor'] = self.supported_ext_color[self.__ext_colorimetry]
            info_frame['AVI_QuantRange'] = self.supported_avi_range[self.__avi_range]
            info_frame['AVI_YCC_Quantization_Range'] = self.supported_avi_ycc_range[self.__avi_ycc_range]
        except KeyError:
            pass
        info_frame_list = list(info_frame.values())
        info_frame_list.insert(0, self.__Buffer_RAM)  # write back to program 0
        self._type_2_command(self.__SIF4, params=info_frame_list)
        self._type_2_command(self.__EXBN4)

    def __setup_display_name(self):
        if self.__video_program in self.__video_format_short_names:
            short_name = self.__video_format_short_names[self.__video_program]
        else:
            short_name = self.__video_program
        if short_name[0:3] == 'EIA':
            short_name = short_name[3:]

        name_string = short_name + ' ' + self.__video_encodings_short_names[self.__video_color_space]
        if len(name_string) >= 20:
            name_string = name_string[:20]
        else:
            name_string += ' ' * (20 - len(name_string))

        self._type_2_command(self.__PNAMES4, params=[self.__Buffer_RAM, '20', name_string])
        self._type_2_command(self.__EXBN4)

    def __copy_timing_info(self, source):
        """
        Instead of executing a pre-defined program, might copy its contents
        Not debugged; not used yet
        """
        h_timing = self._type_3_read_block(self.__LHT4, params=[source])
        h_timing_list = h_timing.split(self.__COMMA_DELIM)
        h_timing_list.insert(0, self.__Buffer_RAM)  # write back to program 0
        self._type_2_command(self.__SHT4, params=h_timing_list)

        v_timing = self._type_3_read_block(self.__LVT4, params=[source])
        v_timing_list = v_timing.split(self.__COMMA_DELIM)
        v_timing_list.insert(0, self.__Buffer_RAM)  # write back to program 0
        self._type_2_command(self.__SVT4, params=v_timing_list)

        # What other info should be copied? InfoFrame?
        self._type_2_command(self.__EXBN4)

    def __copy_info_frame(self, source):
        """
        BUG not tested; not used?
        """
        logger.debug('vg_ASTRO_870 copy_info_frame "%s"' % source)
        info_frame = self._type_3_read_block(self.__LIF4, params=[source])
        # NOTE: THIS WILL FAIL if Vendor_Name or Product contains a ','
        info_frame = info_frame.split(self.__COMMA_DELIM)
        info_frame = collections.OrderedDict(zip(self.__LIF4_InfoFrame_Record_Names, info_frame))
        # Widen Text fields to their fixed-width values
        vendor_name = info_frame['SPD_Vendor_Name_8']
        info_frame['SPD_Vendor_Name_8'] = (vendor_name + '\x00' * 8)[0:8]
        # Widen Text fields to their fixed-width values
        product_name = info_frame['SPD_Product_20']
        info_frame['SPD_Product_20'] = (product_name + '\x00' * 16)[0:16]

        info_frame['AVI_On'] = '1'  # auto-fill-in
        # color_encoding = self.supported_color_encodings[self.__video_color_encoding]
        # if color_encoding == '1':
        # color_encoding = '2'
        # elif color_encoding == '2':
        # color_encoding = '1'
        # info_frame['AVI_RGB_YCbCr'] = color_encoding
        info_frame_list = info_frame.values()
        info_frame_list.insert(0, self.__Buffer_RAM)  # write back to program 0
        self._type_2_command(self.__SIF4, params=info_frame_list)
        self._type_2_command(self.__EXBN4)

    __error_strings = {
        '13': 'H-timing data error',
        '24': 'Error with parameter',
        '25': 'Error with data',
        '31': 'Undefined command was received in terminal mode',
        '33': 'Error in the program number',
        '88': 'Unregistered Audio Data',
        '99': 'Data File not found',
    }

    def __wait_ack_nack(self):
        """
        Wait for either ACK or {STX, ESTS, 2 character Error code, ETX}
        """
        response = str()
        response += self.__recv(4096)
        if response[0] == self.__ACK:
            return
        elif response[0] == self.__STX:
            if response[1] != self.__ESTS:
                raise VGUnexpectedResponseChar('Unexpected second error character "%s"' % response[4])
            if response[4] != self.__ETX:
                raise VGUnexpectedResponseChar('Unexpected last error character "%s"' % response[4])
            self.__err_num = ''.join((response[2], response[3]))
            if self.__err_num in self.__error_strings:
                self.__class__.__display_message(response)
                raise VGErrorResponse('Error Response "%s"' % self.__error_strings[self.__err_num])
            else:
                raise VGErrorResponse('Error Response "%s"' % self.__err_num)
        else:
            raise VGUnexpectedResponseChar('Unexpected character "%s"' % response)

    def __wait_trdt_data(self):
        """
        Wait for a packet consisting of STX, TRDT, data, (ETB or ETX)
        Return Data and an indication if it is the last block.
        """
        response = str()
        while True:
            response += self.__recv(4096)
            if response[0] != self.__STX:
                raise VGUnexpectedResponseChar('Unexpected character "%s"' % response[0])
            if response[1] != self.__TRDT:
                raise VGUnexpectedResponseChar('Unexpected second character "%s"' % response[1])
            if (response[-1] == self.__ETB) or (response[-1] == self.__ETX):
                break
        message = ''.join(response[2:-1])
        return message, (response[-1] == self.__ETX)

    def __wait_data(self):
        """
        Wait for a packet consisting of STX, data, ETX
        """
        response = list()
        response.append(self.__recv(1))
        if response[0] != self.__STX:
            raise VGUnexpectedResponseChar('Unexpected character "%s"' % response[0])
        while True:
            data = self.__recv(1)
            response.append(data)
            if data == self.__ETX:
                break
        message = ''.join(response)
        self.__class__.__display_message(message)
        message = ''.join(response[1:-1])
        return message

    def __send_TRDT_data(self, data, last):
        data_str = self.__STX + self.__TRDT
        data_str += data
        if last:
            data_str += self.__ETX
        else:
            data_str += self.__ETB
        self.__send(data_str)

    def _type_1_enquire(self):
        """
        Type 1: PC sends <ENQ> VG replies <ACK>
        """
        self.__send(self.__ENQ)
        while True:
            result = self.__recv(1)
            if result == self.__ACK:
                return

    def _type_2_command(self, cmd_bytes, params=None, delim=''):
        """
        Type 2: PC sends Command, VG replies ACK or Error
        """
        params = params or []
        if delim == '':
            delim = self.__COMMA_DELIM
        cmd_str = self.__STX + self.__VG4CMD + cmd_bytes
        cmd_str += delim.join(params)
        cmd_str += self.__ETX
        self.__send(cmd_str)
        self.__wait_ack_nack()

    def _type_3_read_block(self, cmd_bytes, params=None, delim=''):
        """
        Type 3: Read a little data
        PC sends Command, VG replies ACK or Error,
        then sends Data using TRDT block
        """
        self._type_2_command(cmd_bytes, params, delim)
        data, ignore = self.__wait_trdt_data()
        return data

    def _type_4_write_block(self, cmd_bytes, params=None, data="", delim=''):
        """
        Type 4: Send a little data
        PC sends Command, VG replies ACK or Error,
        PC sends Data using TRDT, VG replies ACK or Error,
        """
        self._type_2_command(cmd_bytes, params, delim)
        self.__send_TRDT_data(data, True)
        self.__wait_ack_nack()

    def _type_5_read_blocks(self, cmd_bytes, params=None, delim=''):
        """
        Type 5: Read lots of data
        PC sends Command, VG replies ACK or Error,
        VG sends 1 to N blocks of data using TRDT,
        PC sends ACK or Error to each
        """
        self._type_2_command(cmd_bytes, params, delim)
        results = []
        while True:
            data, last = self.__wait_trdt_data()
            results.append(data)
            if last:
                return results

    def _type_6_write_blocks(self, cmd_bytes, params=None, data=None, delim=''):
        """
        Type 6: Send lots of data
        PC sends Command, VG replies ACK or Error,
        PC sends 1 to N blocks of data using TRDT,
        VG sends ACK or Error to each
        """
        data = data or []
        self._type_2_command(cmd_bytes, params, delim)
        last_one = len(data) - 1
        for i, d in enumerate(data):
            last = (i == last_one)
            self.__send_TRDT_data(d, last)
            self.__wait_ack_nack()

    def _type_7_read_alt(self, cmd_bytes, params=None, delim=''):
        """
        Type 7: Read a little data
        PC sends Command, VG replies ACK or Error,
        then sends Data but only sends STX, Data, ETX.  No TRDT
        """
        self._type_2_command(cmd_bytes, params, delim)
        return self.__wait_data()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )

    vg = VG876("172.16.132.250")
    # vg.load('EIA1280x720p@60', 'Color Bar 100/100-H', 'YCbCr422', '8-bit', '8ch', '192 KHz', '24-bit')
    # vg.load_audio('8ch', '48 KHz', '24-bit', 'Internal IEC', "2")
    vg.set_csc_params(basic_color="Extend", ext_color="xvYCC601")
    # print dir(vg)
    vg.load_video('EIA1920x1080p@30', 'Color Bar 100/100-H', 'RGB', '8-bit')