# Unittests #
running tests in this folder:

```
$ python -m unittest -vvv omieMercadoDiarioDBManagerunittest omieMercadoDiarioWebParsersunittest 
```

# Working with the csv via command line using linux:
## getting collumsn from file:
```
cut -d \; -f 1-2 pdbc_stota_20130101.1 > lines.pdbc_stota_20130101.1
```
## replace ; by ':
sed "s/;/:/g" -i lines.pdbc_stota_20130101.1
## adding , to end of line:
sed ':a;N;$!ba;s/\n/,\n/g' -i lines.pdbc_stota_20130101.1
## didn't manage to add ' character to the' thing.

