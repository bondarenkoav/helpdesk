/**
 * Created by ipman on 01.02.2016.
 */

function join(arr /*, separator */) {
    var separator = arguments.length > 1 ? arguments[1] : ", ";
    return arr.filter(function(n){return n}).join(separator);
}

$("#id_AddressObject").suggestions({
    serviceUrl: "https://dadata.ru/api/v2",
    token: "6217fdd8f6360d58dea99eaa3b230271a2f340d8",
    type: "ADDRESS",
    constraints: {locations: { kladr_id: '56' }}, // Ограничение по Оренбургской области
    count: 5,
    /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function(suggestion) {
        console.log(suggestion);
    }
});

$("#id_Client").suggestions({
    serviceUrl: "https://dadata.ru/api/v2",
    token: "6217fdd8f6360d58dea99eaa3b230271a2f340d8",
    type: "NAME",
    count: 5,
       /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function(suggestion) {
        console.log(suggestion);
    }
});

$("#id_Person_FIO").suggestions({
    serviceUrl: "https://dadata.ru/api/v2",
    token: "6217fdd8f6360d58dea99eaa3b230271a2f340d8",
    type: "NAME",
    count: 5,
       /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function(suggestion) {
        console.log(suggestion);
    }
});