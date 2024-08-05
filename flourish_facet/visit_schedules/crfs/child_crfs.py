from edc_visit_schedule import FormsCollection, Crf

child_crfs = FormsCollection(
    Crf(show_order=1, model='flourish_facet.facetchildsociodemographic'),
    Crf(show_order=2, model='flourish_facet.childhivtesting'),
    Crf(show_order=3, model='flourish_facet.childanthropometry'),
    Crf(show_order=4, model='flourish_facet.infantbehaviourquestionnaire'),
    Crf(show_order=5, model='flourish_facet.childneurodevelopmentscreening'),
    Crf(show_order=6, model='flourish_facet.facetcliniciannotes'),
    Crf(show_order=7, model='flourish_facet.facetchildmedicalhistory'),
    Crf(show_order=8, model='flourish_facet.childhivpendingresults', required=False),
    name='facet_enrollment')
