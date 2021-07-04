var ChatPeek = {
  conn: null,
  console_id: "console_peek",
  show_traffic: function(body, type){
    if(body.childNodes.length < 1){
      return;
    }
    var cons = $("#" + ChatPeek.console_id);
    $.each(body.childNodes, function(){
      //                                   ChatPeek.xml2html(Strophe.serialize(this))
      cons.append($("<div class='" + type + "'>" + ChatPeek.pretty_xml(this) + "</div>"));
    });
    cons[0].scrollTop = cons[0].scrollHeight;
  },
  xml2html: function(s){
    return s.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
  },
  pretty_xml: function(xml, level){
    var i, j;
    var result = [];
    if(!level){
      level = 0;
    };
    result.push("<div class='xml_level" + level + "'>");
    result.push("<span class='xml_punc'>&lt;</span>");
    result.push("<span class='xml_tag'>");
    result.push(xml.tagName);
    result.push("</span>");
    // attributes
    var attrs = xml.attributes;
    var attr_lead = [];
    for(i=0; i<xml.tagName.length+1; i++){
      attr_lead.push("&nbsp;");
    }
    for(i=0; i<attrs.length; i++){
      result.push(" <span class='xml_aname'>");
      result.push(attrs[i].nodeName);
      result.push("</span>");
      result.push("<span class='xml_punc'>='</span>");
      result.push("<span class='xml_avalue'>");
      result.push(attrs[i].nodeValue);
      result.push("</span>");
      result.push("<span class='xml_punc'>'</span>");
      if(i !== attrs.length - 1){
        result.push("</div><div class='xml_level" + level + "'>");
        result.push(attr_lead.join(""));
      }
    }
    if(xml.childNodes.length === 0){
      result.push("<span class='xml_punc'>/&gt;</span>");
      result.push("</div>");
    }else{
      result.push("<span class='xml_punc'>&gt;</span>");
      result.push("</div>");
      // children
      $.each(xml.childNodes, function(){
        if(this.nodeType === 1){
          result.push(ChatPeek.pretty_xml(this, level + 1));
        }else if (this.nodeType === 3){
          result.push("<div class='xml_text xml_level" + (level + 1)  + "'>");
          result.push(this.nodeValue);
          result.push("</div>");
        }
      });
      result.push("<div class='xml xml_level" + level + "'>");
      result.push("<span class='xml_punc'>&lt;/</span>");
      result.push("<span class='xml_tag'>");
      result.push(xml.tagName);
      result.push("</span>");
      result.push("<span class='xml_punc'>&gt;</span>");
      result.push("</div>");
    }
    return result.join("");
  },
};