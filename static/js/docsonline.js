// Load Summernote
$('#id_summernote').summernote({
    toolbar: [
        ['style', ['style']],
        ['style', ['bold', 'italic', 'underline', 'strikethrough']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        // ['insert', ['picture']],
        ['table', ['table']],
        // ['view', ['codeview']],
      ],
      height: 650,
      maximumFileSize: '1mb',
      maximumFileSizeError: 'Maximum file size exceeded.',

});

$(document).ready(function(){
    $('#id_summernote').summernote('code');

    $('#tabcomplete').on('click', function(){
        $('#editar .form-group').hide();
        texto = $('#id_summernote').summernote('code');
        $('#completar-text').html(texto);
        $.each($('#completar-text .hl'), function(i){
            $(this).replaceWith('<input class="hl" placeholder="' + $(this).text() + '"></input>');
        });
    });
    
    $('#tabedit').on('click', function(){
        $('#editar .form-group').show();
    });
});

$(document).on('click', function(){

    $('#completar-text input[placeholder]').each(function(){
        $(this).attr('size', $(this).attr('placeholder').length*.9);
    });

    $('#completar-text input').on('change keyup paste', function(){
        $(this).attr('value', $(this).val());
        $(this).html($(this).val());
        $(this).width($(this).prop('scrollWidth'))
    });

    $('#genpdf').on('click', function(){
        $('#completar-text input').each(function(){                        
            $(this).replaceWith('<span>' + $(this).val() + '</span>'); 
        });     
        texto = $('#completar-text').html()
        $('#id_summernote').summernote('code', texto);
    });
});

function pasteHtmlAtCaret(html) {
    var sel, range;
    if (window.getSelection) {
        // IE9 and non-IE
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            range = sel.getRangeAt(0);
            range.deleteContents();
            // Range.createContextualFragment() would be useful here but is
            //non-standard and not supported in all browsers (IE9, for one)
            var el = document.createElement("div");
            el.innerHTML = html;
            var frag = document.createDocumentFragment(), node, lastNode;
            while ( (node = el.firstChild) ) {
                lastNode = frag.appendChild(node);
            }
            range.insertNode(frag);
            // Preserve the selection
            if (lastNode) {
                range = range.cloneRange();
                range.setStartAfter(lastNode);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
            }
        }
    } else if (document.selection && document.selection.type != "Control") {
        // IE < 9
        document.selection.createRange().pasteHTML(html);
    }
}
