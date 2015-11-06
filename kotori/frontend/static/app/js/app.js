// -*- coding: utf-8 -*-
// (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>

var pageTransitions = PageTransitions();

$(document).ready(function() {

    initPages();

    $('.navigate-channels').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        showPage('#channels-list-page', 18);
    });

    $('.add-channel').on('click', function(e) {
        var tpl = _.template($('#channel-configure-template').html());
        var html = tpl({abc: 'def', title: 'NEW', description: 'hello new channel'});
        changeContent('#channel-configure-page', html, 9);
    });

    $('.edit-channel').on('click', function(e) {
        var tpl = _.template($('#channel-configure-template').html());
        var html = tpl({abc: 'def', title: 'FuelCell CSV', description: 'hello existing channel'});
        changeContent('#channel-configure-page', html, 9);
    });

});


function initPages() {
    pageTransitions.init();
}

function addPage(selector, html) {
    $(selector).remove();
    $('#page-wrapper').append(html);
    initPages();
}

function showPage(selector, animation) {
    animation = animation || 9;
    //PageTransitions.toPage(selector, 11);
    pageTransitions.toPage(selector, {animation: animation});
}

function changeContent(selector, html, animation) {
    addPage(selector, html);
    showPage(selector, 9);
}
