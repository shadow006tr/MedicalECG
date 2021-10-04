/*

Function to show the graphs and the data  of the leads  we decided to show in parallel of our main lead

 */
function printOtherGraph(data,positionWhenAdd) {

    console.log('positionWhenAdd',positionWhenAdd);

    positionAddingLeads.push(data['lead_id']);
    console.log("printOther: ", data);

    var chartName = "chart"+ data['lead_id'];
    var labelGraph = "Graph " + data['lead_id'];
    console.log('chartname : ', chartName);

    // we create divs that we add to our graph-container
    var container = document.getElementById('graph-container');
    container.childNodes[1].classList.replace('col-md-9','col-md-6');


    //creation of the div with the graph
    var div = document.createElement("div");
    div.classList.add("col-md-6" , "graph-section");
    div.id = 'graph_number_' + data['lead_id'] ;
    console.log('essai class section');

    var content = '<div class="card">\n' +
        '                        <div class="card-body">\n' +
        '                            <canvas id="'+chartName+'"></canvas>\n' +
        '                        </div>\n' +
        '                    </div>';
    div.innerHTML = content;
    container.appendChild(div);

    var cluster_nav = document.getElementById('clusters_nav');
    var  leadnumber = "Lead_" + data['lead_id'];
    var leadposition = "Lead:"+ positionWhenAdd;
    var li = document.createElement("li");
    var content = '<div id= "nav' + leadnumber+  '"  class="li-cluster" onclick="DisplayContainer('+ positionWhenAdd + ')">\n '+ '<span> '+ leadnumber + '</span>' + '</div>';
    li.innerHTML= content;

    console.log("li",li);
    cluster_nav.appendChild(li);



    var container = document.getElementById('clusters_Maincontainer');
    var div = document.createElement("div");
    var content = '<div id="cluster_nav_'+ positionWhenAdd +'" class="cluster_container">\n' +
         '<div>' +
         '            <button class="btn btn-success  LaunchButton "  id="LaunchButton' + positionWhenAdd + '" onclick="analyze(' + positionWhenAdd + ')" style="margin-left: 80px">\n' +
        '                Launch Analyze\n' +
        '            </button>\n' +
        '\n' +
        '        </div>\n' +
        '\n' +
        '        <div class="cluster-section">\n' +
        '\n' +
        '            <div class="container card-container">\n' +
        '                <div id="cluster_container_'+ positionWhenAdd + '" class="row justify-content-around">\n' +
        '\n' +
        '\n' +
        '                    ---- Clusters: ----\n' +
        '\n' +
        '                </div>\n' +
        '\n' +
        '            </div>\n' +
        '        </div>' +
        '</div>';
     div.style.display = 'none';
    div.innerHTML = content;
    container.appendChild(div);



    //fucntion for the constrcution of the graph

    constructGraph( data['data'], data['pulses'], data['debug'], chartName , labelGraph );

}