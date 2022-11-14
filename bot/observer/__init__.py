uvloop_imported = False

try:
    import uvloop

    uvloop_imported = True

except ImportError:
    pass

if uvloop_imported:
    uvloop.install()
