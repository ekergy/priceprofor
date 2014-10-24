souvenir <- scan("http://robjhyndman.com/tsdldata/data/fancy.dat")
souvenirtimeseries <- ts(souvenir, frequency=12, start=c(1987,1))
plot.ts(souvenirtimeseries)
logsouvenirtimeseries <- log(souvenirtimeseries)
plot.ts (logsouvenirtimeseries)
souvenirtimeseriesforecasts <- HoltWinters(logsouvenirtimeseries)
souvenirtimeseriesforecasts_fitted <- souvenirtimeseriesforecasts$fitted
souvenirtimeseriesforecasts_error <- souvenirtimeseriesforecasts$SSE
plot(souvenirtimeseriesforecasts)
# library("forecast")
souvenirtimeseriesforecasts2 <- forecast.HoltWinters(souvenirtimeseriesforecasts, h=12)
plot.forecast(souvenirtimeseriesforecasts2)
