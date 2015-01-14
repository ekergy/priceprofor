# Priceprofor Gitworkflow:

## main repo github repo:

https://github.com/ekergy/priceprofor

## openshift repo:

ssh://54ae44054382ec0f69000247@price-profor.rhcloud.com/~/git/price.git/

## setting up your local development copy:
Start by clone the github repo:
```
git clone https://github.com/ekergy/priceprofor
```
Add again the github remote url but setting the name github
```
git remote add github https://github.com/ekergy/priceprofor
```
Change the origin remote url to openshift one:
```
git remote set-url origin ssh://54ae44054382ec0f69000247@price-profor.rhcloud.com/~/git/price.git/
```

(optional) if you want you can use the all remote strategy so when you push yo update
all the remotes:
```
git remote add all https://github.com/ekergy/priceprofor
git remote set-url --add all ssh://54ae44054382ec0f69000247@price-profor.rhcloud.com/~/git/price.git/
```

## pulling code:
pulling openshift code:
```
git pull origin master
```
pulling github code:
```
git pull github master
```
the _all_ remote only is set to push from git hub
```
git pull all master
```

## Main development workflow:
Configure the all remote with the 2 url as explained above.
use this to update your local copy:
```
git pull all master
```
and remember that:
```
git push all master
```
will update both github origin (openshift online)

