import urllib2
from bottle import route, run, template, request, static_file
from converter import convert_to_saarland_area, get_object_name

@route('/')
@route('/new/<thing>', method='GET')
def calc_saarland(thing=""):
    result = {}
    thing = ""

    if request.GET.convert:
        # input has been entered: look up ALL the things! \o,

        # get the thing we want to measure in saarlands
        compare_to = request.GET.thing.strip()

        print "received request for %s, converting to Saarland" % compare_to
        if (compare_to):
            area = convert_to_saarland_area(compare_to)
            result["area"] = area
            print "received area result %s, updating website..." % area

            #result["people"] = 123

        # make thing human readable
        thing = get_object_name(compare_to)

    return template('template', thing=thing, result=result)

run(host='0.0.0.0', port=8080, debug=False)
