// Create summernote custom Export button.
var modalbtn = function (context) {
  var ui = $.summernote.ui;
  // create button
  var button = ui.button({
    contents: '<i class="fa fa-file"/>',
    tooltip: 'Export',
    click: function () {
        $('#modalbtn').click();
    }
  });
  return button.render();
}

// Load Summernote
$('#id_summernote').summernote({
    toolbar: [
        ['style', ['style']],
        ['style', ['bold', 'italic', 'underline', 'strikethrough']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['insert', ['picture']],
        ['table', ['table']],
        ['mybutton', ['modalbtn']],
        ['view', ['codeview']],
      ],
      buttons: {
          modalbtn: modalbtn,
        },
      height: 578,
      maximumFileSize: '1mb',
      maximumFileSizeError: 'Maximum file size exceeded.',

});
$('#id_summernote').summernote('code');

// Function change to update the documents variables based on the user input.
// The function matches the user input on the side fields with the corresponding 
// var in the summernote text (id with []). 
function change(){
    var texto = $('#id_summernote').summernote('code');
    var words = texto.match(/\[\w+\]/gi);

    for(var i=0; i < words.length; i++) {
        words[i] = words[i].replace(/\[|\]/g, '');
    }
    var unique_words = words.filter(function(elem, pos) {
        return words.indexOf(elem) == pos;
    }); 

    var fields = document.getElementsByClassName('field form-control');
    replace_words  = [].map.call(fields, function(input) {
        return input.value;
    })
     
    var mapObj = {}
    $.each(replace_words,function(i,val){
        mapObj[unique_words[i]] = val;
    });
    //alert (JSON.stringify(mapObj))

    var re = new RegExp(Object.keys(mapObj).join("|"),"g");
    texto = texto.replace(re, function(matched){
        return mapObj[matched];
    })
    $('#id_summernote').summernote('code', texto);
    $('#id_summernote-textarea').html(texto);
}

// Funtion add to generate the side fields base on the summernote vars with [].
function add() {
    placeholder = $("#placeholder");
    placeholder.empty();
    texto = $('#id_summernote').summernote('code');
    var fields = texto.match(/\[(\w+)\]/g);
    texto = texto.replace(/\[_?/g, '<span class="hl">[_')
    texto = texto.replace(/_?]/g, "_]</span>");
    texto = texto.replace(/<span class="hl"><span class="hl">/g, '<span class="hl">')
    $('#id_summernote').summernote('code', texto);

    var unique_fields = fields.filter(function(elem, pos) {
        return fields.indexOf(elem) == pos;
      }); 
    var uniquelength = unique_fields.length;

    for (var i = 0; i < uniquelength; i++) {
        var element = document.createElement("input");
        var elementlabel = document.createElement("span");
        
        element.setAttribute("type", "input");
        element.setAttribute("class", "field form-control");
        elementlabel.setAttribute("class", "field_label");
        element.setAttribute("name", unique_fields[i]);
        elementlabel.innerHTML = unique_fields[i];

        if ($('input[name="' + unique_fields + '"]').length <= 0) {
           placeholder.append(elementlabel);
           placeholder.append(element);
        }
    }
}
$(document).ready(add);
