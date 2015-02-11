#
####################################################################################
#                                                                                  #   
# Autoregressive and multilayer perceptron artificial neural networks              # 
#                                                                                  #
#                                                                                  #
#                                                                                  #
#                                                                                  #
####################################################################################
#
.onAttach <- 
function(...)
{
    version = library(help = arnn)$info[[1]] 
    version = version[pmatch("Version",version)]
    um = strsplit(version, " ")[[1]]
    version = um[nchar(um) > 0][2]
    #
    cat(paste("This is arnn package", version, "\n"))
}
#
.onLoad <- function(lib,pkg){ library.dynam("arnn","arnn") }
#
####################################################################################
#
coef.arnn      <- function(object, ...) { object$par       }
fitted.arnn    <- function(object, ...) { object$fitted    }
residuals.arnn <- function(object, ...) { object$residuals }
logLik.arnn    <- function(object, ...) { structure( object$loglik,df=length(object$par),class="logLik") }
#
summary.arnn   <- function(object, ...) 
{
    require(forecast)
    print(object) 
    cat("\nIn-sample error measures:\n")
    print(accuracy(object))
}
#
print.arnn <-
function (x, ...) 
{
    cat(paste("\nMethod:", x$method, "\n\n"))
    cat(paste("Call:\n", deparse(x$call), "\n\n"))
    cat("Parameters:\n\n")
    print(coef(x))
    cat("\n\n")
    cat("Sigma^2 estimated as: ", as.character(x$sigma^2))
    cat("\n\n")
    cat("LogL: ", as.character(x$loglik))
    cat("\n\n")
    cat("Information Criteria:\n")
    print(x$IC)
    cat("\n\n")
}
#----------------------------------------------------------------------------------#
arnn <-
function(x, lags = NULL, isMLP = FALSE, H = 1, w.max = 1.0, restarts = 1, seed = NULL,
    lambda = 0, model = NULL,  optim.control = list()) 
{    
  #
  ################################################################################
  #                                                                              #
  #                             Funciones auxiliares                             # 
  #                                                                              #
	################################################################################
  #
  lagvector <- function(x, lags) 	
  {    
		z = embed(x, max(lags)+1)
		return (z[,lags+1])
  }	
	#
  #-------------------------------------------------------------------------------
  #	
	object2par <- function(object) 
  {
		if (isMLP == TRUE)
		{
			return(c( object$M, c(object$Wih), c(object$Wbh), c(object$Who), object$Wbo))
		}
		return(c( object$M, c(object$Wio), c(object$Wih), c(object$Wbh), c(object$Who), object$Wbo))
	}
	#
  #-------------------------------------------------------------------------------
  #	
	par2object <- function(object, par) 
  {
		k = 2  
    ###
    object$M     = par[1]        
    ###
    if (isMLP == FALSE)
    {
      object$Wio = matrix( data = par[k:(k + object$nlags - 1)], 
                           nrow = object$nlags, 
                           ncol = 1)        
      k          = k + object$nlags
    }
    else        
    {
      object$Wio = matrix( 0, nrow = object$nlags, ncol = 1)        
    }        
    ###
    if( object$H > 0)
    {
      ###
		  object$Wih = matrix( data = par[k:(k + object$H * object$nlags - 1)], 
                         nrow = object$nlags, 
		                     ncol = object$H)        
		  k          = k + object$H * object$nlags
      ###
		  object$Wbh = matrix( data = par[k:(k+object$H-1)],
                           nrow = object$H,
                           ncol = 1)
		  k          = k + object$H
		  ###
      object$Who = matrix( data = par[k:(k+object$H-1)],
                           nrow = object$H,
                           ncol = 1)
		  k          = k + object$H
    }
		###
    object$Wbo = par[k]
    ###
		return(object)
	}
	#
  #-------------------------------------------------------------------------------
  #	
	fn.foptim = function(w) 
  {
		object = par2object(object, w)
		object = arnn(x = object$x, model = object)		        
		return((1 - object$lambda) * object$sigma ^ 2 + object$lambda * sum( abs(w[-1])))		
	}
	#
  ################################################################################
	#                                                                              #
  #                            Cuerpo de la funcion                              # 
  #                                                                              #
	################################################################################
  #
  if (!exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)) { runif(1) }
  if (is.null(seed)) 
  {
    RNGstate <- get(".Random.seed", envir = .GlobalEnv)
  }
  else 
  {
    R.seed <- get(".Random.seed", envir = .GlobalEnv)
    set.seed(seed)
    RNGstate <- structure(seed, kind = as.list(RNGkind()))
    on.exit(assign(".Random.seed", R.seed, envir = .GlobalEnv))
  }
  #
  #
  #
	if (is.null(model)) 
  {		
		object = list( x = x, lags = lags, nlags = length(lags), 
                   maxlag = max(lags), call = match.call(),            
                   method   = "arnn",             
                   restarts = restarts,
                   H        = H,                  # número de neuronas en la capa oculta			
                   lambda   = lambda,             # parámetro de regularización
                   numpar   = 1 + 1 + 2 * H + length(lags) * H)  
		#
    if( isMLP == FALSE )
    {
      object$numpar = object$numpar + object$nlags
    }
    #
		object = structure(object, class = "arnn")		
		runopt = TRUE 						
		#
	}
  else
  {
		object      = model
		object$x    = x
		object$call = match.call()
		runopt      = FALSE
	}
	#
  #--------------------------------------------------------------------------------
  #
	X.lagged = lagvector(object$x, object$lags)
  y = x[(max(object$lags)+1):length(x)]
  L = nrow(X.lagged)
	#
	#--------------------------------------------------------------------------------
	# 
	if (runopt == TRUE) 
  {		
    for( irestart in 1:restarts)
    {
      wopt = optim( par     = runif(object$numpar, min = -w.max, max = w.max), 
                    fn      = fn.foptim,
                    method  = "BFGS", 
                    control = optim.control )
                          
      u =  fn.foptim(wopt$par)

      if (irestart == 1 || u < u.opt )
      {
        w.gopt = wopt
        u.opt  = u
      }
    }                 
    object = par2object(object, w.gopt$par)        
		#
    #----------------------------------------------------------------------------
    #   
    names(object$M   ) = "M"
    names(object$Wbo ) = "Wbo"
    names(object$Wio ) = paste("Wio[", object$lags, "]", sep = "")
    if(object$H > 0)
    {
      names(object$Wbh ) = paste("Wbh[", 1:object$H,  "]", sep = "")
      names(object$Who ) = paste("Who[", 1:object$H,  "]", sep = "")
      names(object$Wih ) = paste("Wih[", 
                                 matrix( rep(1:object$nlags, object$H),  object$nlags, object$H), 
                                 ",", 
                                 t(matrix( rep(1:object$H, object$nlags), object$H, object$nlags)), 
                                 "]", sep = "" )
        
      #
      object$par = c( object$M, c(object$Wio), c(object$Wih), c(object$Wbh), 
                      c(object$Who), object$Wbo)
    }
    else
    {
      object$par = c( object$M, c(object$Wio), object$Wbo)
    } 
	}
	#
	#--------------------------------------------------------------------------------
	#		
  if( object$H > 0)
  {
	  f = X.lagged %*% object$Wih + t(matrix(rep(object$Wbh, L), nrow = object$H, ncol = L))
	  f = (1 / (1 + exp(-f))) ^ object$M 		
	  f = f %*% object$Who + object$Wbo + X.lagged %*% object$Wio
  }
  else
  {
    f = object$Wbo + X.lagged %*% object$Wio
  }
	#
	#--------------------------------------------------------------------------------
	#		
  response         = y
  residuals        = y - f
  object$sigma     = sqrt(sum(residuals ^ 2) / (length(residuals) - 1))
  if(L >= object$maxlag)
  {
    object$loglik    = -0.5 * (L - object$maxlag) * (log(2 * pi) + log(object$sigma^2)) - 
                       0.5 * sum(residuals^2) / object$sigma^2
    p                = 1 + object$nlags
	  N                = L - object$maxlag   
    AK               = -2 * object$loglik  + 2 * object$numpar                                 
    AKc              = -2 * object$loglik  + 2 * object$numpar * (N / (N - object$numpar - 1))
    HQ               = -2 * object$loglik  + 2 * object$numpar * log(log(L - object$maxlag)) 
    SC               = -2 * object$loglik  +     object$numpar * log(N)              
    object$IC        = c(AK, AKc, HQ, SC)
    names(object$IC) = c("AK", "AKc", "HQ", "SC")
  }
  else
  {
    object$loglik = AK = AKc = HQ = SC = NULL
  }
  #
  #--------------------------------------------------------------------------------
  #    	
  frequency        = attributes(object$x)$tsp[3]    
	start            = attributes(object$x)$tsp[1] + object$maxlag / frequency    
  object$response  = ts(response,  start = start, frequency = frequency)
  object$fitted    = ts(f,         start = start, frequency = frequency)
  object$residuals = ts(residuals, start = start, frequency = frequency)
  #
	return(object)
}
#----------------------------------------------------------------------------------#
simulate.arnn <-
function (object, nsim = 1000, seed = NULL, h = length(object$x),  
    bootstrap = FALSE, ...) 
{
    #-------------------------------------------------------------------------------
    if (!exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)) { runif(1) }
    if (is.null(seed)) 
    {
        RNGstate <- get(".Random.seed", envir = .GlobalEnv)
    }
    else 
    {
        R.seed <- get(".Random.seed", envir = .GlobalEnv)
        set.seed(seed)
        RNGstate <- structure(seed, kind = as.list(RNGkind()))
        on.exit(assign(".Random.seed", R.seed, envir = .GlobalEnv))
    }
    #-------------------------------------------------------------------------------
    if (bootstrap) 
    {
        e = matrix(sample(object$residuals, h * nsim, replace = TRUE), 
            nrow = h, ncol = nsim)
    }
    else 
    {
        e = matrix(rnorm(h * nsim, 0, object$sigma), 
            nrow = h, ncol = nsim)
    }
    #-------------------------------------------------------------------------------
    To = length(object$x)
    s = matrix(NA, nrow = h, ncol = nsim)
    #
	for (iserie in 1:nsim) 
    {
		x.sim = c(object$x, rep(NULL, times = h))
        #
		for (k in 1:h) 
        {
			X = x.sim[(To + k) - object$lags]            
			#######################################################################
			f = matrix(NA, nrow = 1, ncol = object$H)
			for(i in 1:object$H) {
				f[,i] = X %*% object$Wih[,i]+ object$Wbh[i]
				f[,i] = (1 / (1 + exp(-f[,i])))^object$M
			}
			f = f %*% object$Who + object$Wbo + X %*% object$Wio
			#######################################################################
			x.sim[To + k] = f + e[k, iserie]
		}
		s[, iserie] = x.sim[(To + 1):(To + h)]
	}
	return(s)
}
#----------------------------------------------------------------------------------#
forecast.arnn <-
function (object, h = 10, level = c(80, 95), fan = FALSE, bootstrap = FALSE, 
    seed = 1234, npaths = 5000, ...) 
{
    if (fan) 
        level <- seq(51, 99, by = 3)
    else 
    {
        if (min(level) > 0 & max(level) < 1) 
            level <- 100 * level
        else if (min(level) < 0 | max(level) > 99.99) 
            stop("Confidence limit out of range")
    }
    nconf = length(level)
    lower = upper = matrix(NA, nrow = h, ncol = nconf)
    m = rep(0, h)
	#######################################################################
    paths = simulate(object = object, npaths = npaths, seed = seed, h = h, bootstrap = bootstrap)
	#######################################################################
    for (k in 1:h) {
        m[k] = quantile(paths[, k], 0.5)
        lower[k, ] = quantile(paths[, k], (1 - level/100))
        upper[k, ] = quantile(paths[, k], level/100)
    }
    colnames(lower) = colnames(upper) = paste(level, "%", sep = "")
    #
    #
    #
    result           = list()
    result$model     = object
    result$method    = object$method    
    result$level     = level
    result$x         = object$x
    result$residuals = residuals(object)
    result$fitted    = fitted(object)    
    #
    frequency        = attributes(object$x)$tsp[3]
    start            = attributes(object$x)$tsp[1] + length(object$x)/frequency
    result$mean      = ts(data = m, start = start, frequency = frequency)
    result$lower     = ts(data = lower, start = start, frequency = frequency)
    result$upper     = ts(data = upper, start = start, frequency = frequency)
    #
    result = structure(result, class = "forecast")
    return(result)
}
#----------------------------------------------------------------------------------#

#
#### First 80 points are used to fit the model
#x <- ts(WWWusage[1:80], s = 1, f = 1)
#
#### A mlp neural network is fitted
#fit <- arnn(x=x, lags=1:4, isMLP=FALSE, H=2, w.max=1e-3,     
#    restarts=10, seed = 1234, lambda=0, optim.control=list(maxit=200))
#
#### information about the fitted model
#summary(fit)    
#    
#### in-sample errors    
#accuracy(fit)
#
#### out-of-sample errors
#fit1 <- arnn(x = WWWusage, model = fit)
#accuracy( fitted(fit1)[76:96], WWWusage[81:100] )
#
#### one-step forecasts plot
#plot(WWWusage)
#lines(fitted(fit1), col = 'red')
#grid()
#
#### multi-step forecast plot
#plot(forecast(fit, h=20, level=90, fan=FALSE, bootstrap=FALSE, 
#    seed=1234, npaths=1000))
#grid()
#





