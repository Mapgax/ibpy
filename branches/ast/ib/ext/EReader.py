#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## Source file: "EReader.java"
## Target file: "EReader.py"
##
## Original file copyright original author(s).
## This file copyright Troy Melhase <troy@gci.net>.
##

from ib.aux import Boolean, Double, DataInputStream, Integer, StringBuffer, Thread
from ib.aux.overloading import overloaded

from ib.ext.Contract import Contract
from ib.ext.ContractDetails import ContractDetails
from ib.ext.Order import Order

class EReader(Thread):
    """ generated source for EReader

    """
    TICK_PRICE = 1
    TICK_SIZE = 2
    ORDER_STATUS = 3
    ERR_MSG = 4
    OPEN_ORDER = 5
    ACCT_VALUE = 6
    PORTFOLIO_VALUE = 7
    ACCT_UPDATE_TIME = 8
    NEXT_VALID_ID = 9
    CONTRACT_DATA = 10
    EXECUTION_DATA = 11
    MARKET_DEPTH = 12
    MARKET_DEPTH_L2 = 13
    NEWS_BULLETINS = 14
    MANAGED_ACCTS = 15
    RECEIVE_FA = 16
    HISTORICAL_DATA = 17
    BOND_CONTRACT_DATA = 18
    SCANNER_PARAMETERS = 19
    SCANNER_DATA = 20
    TICK_OPTION_COMPUTATION = 21
    TICK_GENERIC = 45
    TICK_STRING = 46
    m_parent = None
    m_dis = None

    def parent(self):
        return self.m_parent

    def eWrapper(self):
        return self.parent().wrapper()

    @overloaded
    def __init__(self, parent, dis):
        self.__init__("EReader", parent, dis)

    @__init__.register(object, str, object, DataInputStream)
    def __init___0(self, name, parent, dis):
        Thread.__init__(self, name, parent, dis)
        self.setName(name)
        self.m_parent = parent
        self.m_dis = dis

    def run(self):
        try:
            while not self.isInterrupted() and self.processMsg(self.readInt()):
                pass
        except (Exception, ), ex:
            self.parent().wrapper().error(ex)
            self.parent().wrapper().connectionClosed()
        self.m_parent.close()

    def processMsg(self, msgId):
        if (msgId == -1):
            return False
        if msgId == self.TICK_PRICE:
            version = self.readInt()
            tickerId = self.readInt()
            tickType = self.readInt()
            price = self.readDouble()
            size = 0
            if version >= 2:
                size = self.readInt()
            canAutoExecute = 0
            if version >= 3:
                canAutoExecute = self.readInt()
            self.eWrapper().tickPrice(tickerId, tickType, price, canAutoExecute)
            if version >= 2:
                sizeTickType = -1
                if tickType == 1:
                    sizeTickType = 0
                elif tickType == 2:
                    sizeTickType = 3
                elif tickType == 4:
                    sizeTickType = 5
                if (sizeTickType != -1):
                    self.eWrapper().tickSize(tickerId, sizeTickType, size)
        elif msgId == self.TICK_SIZE:
            version = self.readInt()
            tickerId = self.readInt()
            tickType = self.readInt()
            size = self.readInt()
            self.eWrapper().tickSize(tickerId, tickType, size)
        elif msgId == self.TICK_OPTION_COMPUTATION:
            version = self.readInt()
            tickerId = self.readInt()
            tickType = self.readInt()
            impliedVol = self.readDouble()
            if impliedVol < 0:
                impliedVol = Double.MAX_VALUE
            delta = self.readDouble()
            if Math.abs(delta) > 1:
                delta = Double.MAX_VALUE
            modelPrice = float()
            pvDividend = float()
            if (tickType == TickType.MODEL_OPTION):
                modelPrice = self.readDouble()
                pvDividend = self.readDouble()
            else:
                modelPrice = pvDividend = Double.MAX_VALUE
            self.eWrapper().tickOptionComputation(tickerId, tickType, impliedVol, delta, modelPrice, pvDividend)
        elif msgId == self.TICK_GENERIC:
            version = self.readInt()
            tickerId = self.readInt()
            tickType = self.readInt()
            value = self.readDouble()
            self.eWrapper().tickGeneric(tickerId, tickType, value)
        elif msgId == self.TICK_STRING:
            version = self.readInt()
            tickerId = self.readInt()
            tickType = self.readInt()
            value = self.readStr()
            self.eWrapper().tickString(tickerId, tickType, value)
        elif msgId == self.ORDER_STATUS:
            version = self.readInt()
            id = self.readInt()
            status = self.readStr()
            filled = self.readInt()
            remaining = self.readInt()
            avgFillPrice = self.readDouble()
            permId = 0
            if version >= 2:
                permId = self.readInt()
            parentId = 0
            if version >= 3:
                parentId = self.readInt()
            lastFillPrice = 0
            if version >= 4:
                lastFillPrice = self.readDouble()
            clientId = 0
            if version >= 5:
                clientId = self.readInt()
            self.eWrapper().orderStatus(id, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId)
        elif msgId == self.ACCT_VALUE:
            version = self.readInt()
            key = self.readStr()
            val = self.readStr()
            cur = self.readStr()
            accountName = None
            if version >= 2:
                accountName = self.readStr()
            self.eWrapper().updateAccountValue(key, val, cur, accountName)
        elif msgId == self.PORTFOLIO_VALUE:
            version = self.readInt()
            contract = Contract()
            contract.m_symbol = self.readStr()
            contract.m_secType = self.readStr()
            contract.m_expiry = self.readStr()
            contract.m_strike = self.readDouble()
            contract.m_right = self.readStr()
            contract.m_currency = self.readStr()
            if version >= 2:
                contract.m_localSymbol = self.readStr()
            position = self.readInt()
            marketPrice = self.readDouble()
            marketValue = self.readDouble()
            averageCost = 0.0
            unrealizedPNL = 0.0
            realizedPNL = 0.0
            if version >= 3:
                averageCost = self.readDouble()
                unrealizedPNL = self.readDouble()
                realizedPNL = self.readDouble()
            accountName = None
            if version >= 4:
                accountName = self.readStr()
            self.eWrapper().updatePortfolio(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName)
        elif msgId == self.ACCT_UPDATE_TIME:
            version = self.readInt()
            timeStamp = self.readStr()
            self.eWrapper().updateAccountTime(timeStamp)
        elif msgId == self.ERR_MSG:
            version = self.readInt()
            if version < 2:
                msg = self.readStr()
                self.m_parent.error(msg)
            else:
                id = self.readInt()
                errorCode = self.readInt()
                errorMsg = self.readStr()
                self.m_parent.error(id, errorCode, errorMsg)
        elif msgId == self.OPEN_ORDER:
            version = self.readInt()
            order = Order()
            order.m_orderId = self.readInt()
            contract = Contract()
            contract.m_symbol = self.readStr()
            contract.m_secType = self.readStr()
            contract.m_expiry = self.readStr()
            contract.m_strike = self.readDouble()
            contract.m_right = self.readStr()
            contract.m_exchange = self.readStr()
            contract.m_currency = self.readStr()
            if version >= 2:
                contract.m_localSymbol = self.readStr()
            order.m_action = self.readStr()
            order.m_totalQuantity = self.readInt()
            order.m_orderType = self.readStr()
            order.m_lmtPrice = self.readDouble()
            order.m_auxPrice = self.readDouble()
            order.m_tif = self.readStr()
            order.m_ocaGroup = self.readStr()
            order.m_account = self.readStr()
            order.m_openClose = self.readStr()
            order.m_origin = self.readInt()
            order.m_orderRef = self.readStr()
            if version >= 3:
                order.m_clientId = self.readInt()
            if version >= 4:
                order.m_permId = self.readInt()
                order.m_ignoreRth = (self.readInt() == 1)
                order.m_hidden = (self.readInt() == 1)
                order.m_discretionaryAmt = self.readDouble()
            if version >= 5:
                order.m_goodAfterTime = self.readStr()
            if version >= 6:
                order.m_sharesAllocation = self.readStr()
            if version >= 7:
                order.m_faGroup = self.readStr()
                order.m_faMethod = self.readStr()
                order.m_faPercentage = self.readStr()
                order.m_faProfile = self.readStr()
            if version >= 8:
                order.m_goodTillDate = self.readStr()
            if version >= 9:
                order.m_rule80A = self.readStr()
                order.m_percentOffset = self.readDouble()
                order.m_settlingFirm = self.readStr()
                order.m_shortSaleSlot = self.readInt()
                order.m_designatedLocation = self.readStr()
                order.m_auctionStrategy = self.readInt()
                order.m_startingPrice = self.readDouble()
                order.m_stockRefPrice = self.readDouble()
                order.m_delta = self.readDouble()
                order.m_stockRangeLower = self.readDouble()
                order.m_stockRangeUpper = self.readDouble()
                order.m_displaySize = self.readInt()
                order.m_rthOnly = self.readBoolFromInt()
                order.m_blockOrder = self.readBoolFromInt()
                order.m_sweepToFill = self.readBoolFromInt()
                order.m_allOrNone = self.readBoolFromInt()
                order.m_minQty = self.readInt()
                order.m_ocaType = self.readInt()
                order.m_eTradeOnly = self.readBoolFromInt()
                order.m_firmQuoteOnly = self.readBoolFromInt()
                order.m_nbboPriceCap = self.readDouble()
            if version >= 10:
                order.m_parentId = self.readInt()
                order.m_triggerMethod = self.readInt()
            if version >= 11:
                order.m_volatility = self.readDouble()
                order.m_volatilityType = self.readInt()
                if (version == 11):
                    receivedInt = self.readInt()
                    order.m_deltaNeutralOrderType = "NONE" if (receivedInt == 0) else "MKT"
                else:
                    order.m_deltaNeutralOrderType = self.readStr()
                    order.m_deltaNeutralAuxPrice = self.readDouble()
                order.m_continuousUpdate = self.readInt()
                if (self.m_parent.serverVersion() == 26):
                    order.m_stockRangeLower = self.readDouble()
                    order.m_stockRangeUpper = self.readDouble()
                order.m_referencePriceType = self.readInt()
            if version >= 13:
                order.m_trailStopPrice = self.readDouble()
            self.eWrapper().openOrder(order.m_orderId, contract, order)
        elif msgId == self.NEXT_VALID_ID:
            version = self.readInt()
            orderId = self.readInt()
            self.eWrapper().nextValidId(orderId)
        elif msgId == self.SCANNER_DATA:
            contract = ContractDetails()
            version = self.readInt()
            tickerId = self.readInt()
            numberOfElements = self.readInt()
            ## for-while
            ctr = 0
            while ctr < numberOfElements:
                rank = self.readInt()
                contract.m_summary.m_symbol = self.readStr()
                contract.m_summary.m_secType = self.readStr()
                contract.m_summary.m_expiry = self.readStr()
                contract.m_summary.m_strike = self.readDouble()
                contract.m_summary.m_right = self.readStr()
                contract.m_summary.m_exchange = self.readStr()
                contract.m_summary.m_currency = self.readStr()
                contract.m_summary.m_localSymbol = self.readStr()
                contract.m_marketName = self.readStr()
                contract.m_tradingClass = self.readStr()
                distance = self.readStr()
                benchmark = self.readStr()
                projection = self.readStr()
                self.eWrapper().scannerData(tickerId, rank, contract, distance, benchmark, projection)
                ctr += 1
        elif msgId == self.CONTRACT_DATA:
            version = self.readInt()
            contract = ContractDetails()
            contract.m_summary.m_symbol = self.readStr()
            contract.m_summary.m_secType = self.readStr()
            contract.m_summary.m_expiry = self.readStr()
            contract.m_summary.m_strike = self.readDouble()
            contract.m_summary.m_right = self.readStr()
            contract.m_summary.m_exchange = self.readStr()
            contract.m_summary.m_currency = self.readStr()
            contract.m_summary.m_localSymbol = self.readStr()
            contract.m_marketName = self.readStr()
            contract.m_tradingClass = self.readStr()
            contract.m_conid = self.readInt()
            contract.m_minTick = self.readDouble()
            contract.m_multiplier = self.readStr()
            contract.m_orderTypes = self.readStr()
            contract.m_validExchanges = self.readStr()
            if version >= 2:
                contract.m_priceMagnifier = self.readInt()
            self.eWrapper().contractDetails(contract)
        elif msgId == self.BOND_CONTRACT_DATA:
            version = self.readInt()
            contract = ContractDetails()
            contract.m_summary.m_symbol = self.readStr()
            contract.m_summary.m_secType = self.readStr()
            contract.m_summary.m_cusip = self.readStr()
            contract.m_summary.m_coupon = self.readDouble()
            contract.m_summary.m_maturity = self.readStr()
            contract.m_summary.m_issueDate = self.readStr()
            contract.m_summary.m_ratings = self.readStr()
            contract.m_summary.m_bondType = self.readStr()
            contract.m_summary.m_couponType = self.readStr()
            contract.m_summary.m_convertible = self.readBoolFromInt()
            contract.m_summary.m_callable = self.readBoolFromInt()
            contract.m_summary.m_putable = self.readBoolFromInt()
            contract.m_summary.m_descAppend = self.readStr()
            contract.m_summary.m_exchange = self.readStr()
            contract.m_summary.m_currency = self.readStr()
            contract.m_marketName = self.readStr()
            contract.m_tradingClass = self.readStr()
            contract.m_conid = self.readInt()
            contract.m_minTick = self.readDouble()
            contract.m_orderTypes = self.readStr()
            contract.m_validExchanges = self.readStr()
            if version >= 2:
                contract.m_summary.m_nextOptionDate = self.readStr()
                contract.m_summary.m_nextOptionType = self.readStr()
                contract.m_summary.m_nextOptionPartial = self.readBoolFromInt()
                contract.m_summary.m_notes = self.readStr()
            self.eWrapper().bondContractDetails(contract)
        elif msgId == self.EXECUTION_DATA:
            version = self.readInt()
            orderId = self.readInt()
            contract = Contract()
            contract.m_symbol = self.readStr()
            contract.m_secType = self.readStr()
            contract.m_expiry = self.readStr()
            contract.m_strike = self.readDouble()
            contract.m_right = self.readStr()
            contract.m_exchange = self.readStr()
            contract.m_currency = self.readStr()
            contract.m_localSymbol = self.readStr()
            exec_ = Execution()
            exec_.m_orderId = orderId
            exec_.m_execId = self.readStr()
            exec_.m_time = self.readStr()
            exec_.m_acctNumber = self.readStr()
            exec_.m_exchange = self.readStr()
            exec_.m_side = self.readStr()
            exec_.m_shares = self.readInt()
            exec_.m_price = self.readDouble()
            if version >= 2:
                exec_.m_permId = self.readInt()
            if version >= 3:
                exec_.m_clientId = self.readInt()
            if version >= 4:
                exec_.m_liquidation = self.readInt()
            self.eWrapper().execDetails(orderId, contract, exec_)
        elif msgId == self.MARKET_DEPTH:
            version = self.readInt()
            id = self.readInt()
            position = self.readInt()
            operation = self.readInt()
            side = self.readInt()
            price = self.readDouble()
            size = self.readInt()
            self.eWrapper().updateMktDepth(id, position, operation, side, price, size)
        elif msgId == self.MARKET_DEPTH_L2:
            version = self.readInt()
            id = self.readInt()
            position = self.readInt()
            marketMaker = self.readStr()
            operation = self.readInt()
            side = self.readInt()
            price = self.readDouble()
            size = self.readInt()
            self.eWrapper().updateMktDepthL2(id, position, marketMaker, operation, side, price, size)
        elif msgId == self.NEWS_BULLETINS:
            version = self.readInt()
            newsMsgId = self.readInt()
            newsMsgType = self.readInt()
            newsMessage = self.readStr()
            originatingExch = self.readStr()
            self.eWrapper().updateNewsBulletin(newsMsgId, newsMsgType, newsMessage, originatingExch)
        elif msgId == self.MANAGED_ACCTS:
            version = self.readInt()
            accountsList = self.readStr()
            self.eWrapper().managedAccounts(accountsList)
        elif msgId == self.RECEIVE_FA:
            version = self.readInt()
            faDataType = self.readInt()
            xml = self.readStr()
            self.eWrapper().receiveFA(faDataType, xml)
        elif msgId == self.HISTORICAL_DATA:
            version = self.readInt()
            reqId = self.readInt()
            startDateStr = ""
            endDateStr = ""
            completedIndicator = "finished"
            if version >= 2:
                startDateStr = self.readStr()
                endDateStr = self.readStr()
                completedIndicator += "-" + startDateStr + "-" + endDateStr
            itemCount = self.readInt()
            ## for-while
            ctr = 0
            while ctr < itemCount:
                date = self.readStr()
                open = self.readDouble()
                high = self.readDouble()
                low = self.readDouble()
                close = self.readDouble()
                volume = self.readInt()
                WAP = self.readDouble()
                hasGaps = self.readStr()
                barCount = -1
                if version >= 3:
                    barCount = self.readInt()
                self.eWrapper().historicalData(reqId, date, open, high, low, close, volume, barCount, WAP, Boolean.valueOf(hasGaps).booleanValue())
                ctr += 1
            self.eWrapper().historicalData(reqId, completedIndicator, -1, -1, -1, -1, -1, -1, -1, False)
        elif msgId == self.SCANNER_PARAMETERS:
            version = self.readInt()
            xml = self.readStr()
            self.eWrapper().scannerParameters(xml)
        else:
            self.m_parent.error(EClientErrors.NO_VALID_ID, EClientErrors.UNKNOWN_ID.code(), EClientErrors.UNKNOWN_ID.msg())
            return False
        return True

    def readStr(self):
        buf = StringBuffer()
        while True:
            c = self.m_dis.readByte()
            if (c == 0):
                break
            buf.append(c)
        strval = str(buf)
        return None if strval == 0 else strval

    def readBoolFromInt(self):
        strval = self.readStr()
        return False if strval is None else (Integer.parseInt(strval) != 0)

    def readInt(self):
        strval = self.readStr()
        return 0 if strval is None else Integer.parseInt(strval)

    def readLong(self):
        strval = self.readStr()
        return 0l if strval is None else Long.parseLong(strval)

    def readDouble(self):
        strval = self.readStr()
        return 0 if strval is None else Double.parseDouble(strval)

