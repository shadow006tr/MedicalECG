/*
The function receives all the data of the clusters and constructs the page with the cards of the clsuters
and the different functions to analyse and observe the results of the analyse
 */

function print_cluster_data(data , pulse_length , positionWhenAdd) {
    console.log("Purrrre",positionWhenAdd);
    console.log('datax');



    // create div for card and add  it to the container of the cards
    var container = document.getElementById('cluster_container_' + positionWhenAdd);

    for (var i = 0 ; i < data.clusters.length ; i++){
        // var clusterPulse = data['clusters'][i][1];

        var list_wave = '';
        console.log(data['clusters'][i][1]);
        var pulseList = data['clusters'][i][1];
        var help = data['clusters'][i][1];


        var sorted= false;

        console.log(pulseList[0]);

        console.log('help',help[0]);
        console.log('sotred', sorted);

        listwaves = getListWaves(data['clusters'][i][1],sorted,positionWhenAdd);




        //percentage of the waves of this cluster on the total waves of the lead
        var percentage = Number((data['clusters'][i][2]/pulse_length * 100).toFixed(2));


        //creation of the card
        var div = document.createElement("div");
        div.className = "card card-cluster mx-3 my-2";
        div.innerHTML = '<h5 class="card-title mx-auto p-2">' + 'Cluster n: '+(i+1) + '</h5>\n' +
            '                       <canvas id="myChartDelegate'+(i+1).toString()+'::'+positionWhenAdd.toString()+'"></canvas>\n'+
            '                       <div class="card-body">\n' +
            '                           <p class="card-text"><strong>Number of waves : </strong> '+ data['clusters'][i][2]+'</p>\n' +
            '                           <p class="card-text"><strong>Percentage of waves: </strong>'+percentage+'% </p>\n' +

            ' <form> <input onchange="sort(this,['+ pulseList + '],positionWhenAdd)" type="checkbox" id="sorted'+(i+1).toString()+'::'+positionWhenAdd.toString()+'">\n' +
             '<label  for="sorted">Waves sorted</label></form>\n' +
            '                           <div class="list-view-box" id="cluster-view-box'+(i+1).toString()+'::'+positionWhenAdd.toString()+'">\n' +
                                         listwaves+
            '                         </div>\n' +
            '                         </div>\n' +
            '                    <div class="card-footer">\n' +
            '                      <button id="view-wave-btn'+(i+1).toString()+'::'+positionWhenAdd.toString()+'" class="btn btn-warning" onclick="viewWave('+ (i+1).toString()+','+ '['+data['clusters'][i][1] +']'  + ','+ positionWhenAdd+ ')"  >Print all waves on graph</button>\n' +
            '                    </div>';
        container.appendChild(div);


        console.log("delegate", data['clusters'][i][4]);

        var delegate = 'Wave ' + data['clusters'][i][4];
        //creation of a little graph to show the delegate of each cluster
        var ctx = document.getElementById('myChartDelegate'+(i+1).toString()+'::'+positionWhenAdd.toString()).getContext('2d');
        var labelarray = new Array(300);
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                labels: labelarray,
                datasets: [{
                    // label: 'My First dataset',
                    backgroundColor: 'transparent',
                    borderColor: 'rgb(63,148,255)',
                    data: data['clusters'][i][5],
                    label: delegate
                }]
            },

        // Configuration options go here
            options: {
                legend: {
                     display: true
                },

                elements: {
                        point:{
                            radius: 0
                        }
                    },
                scales: {
                yAxes:[{
                     gridLines: {
                     display:true,
                    color:"rgba(255,99,132,0.2)"
                             }
                        }],
                 xAxes:[{
                        gridLines: {
                              display:false
                                 },
                         ticks: {
                                display: false
                            }
                        }]
                    }


            }
        });


    }

 }

 function sort(e,pulses,position)
 {
     console.log(e);
     console.log('checked',e.checked);
     console.log('lespulses',pulses);
     let listwaves = getListWaves(pulses,e.checked,position);
     let  id = e.id.replace('sorted','cluster-view-box');
     console.log('id',id);
     let wavecontainer = document.getElementById(id);

     wavecontainer.innerHTML = listwaves;

 }

 function getListWaves(pulses,sorted,positionWhenAdd)
 {

     console.log("Je comprends pas",positionWhenAdd);
     let list_wave = '';
     if(sorted)
        {
             var pulseListSorted = pulses.sort(function(a, b) {
              return a - b;
            });

             for (var j= 0 ; j < pulseListSorted.length ; j++)
             {
            list_wave += '<li class="list-group-item list-view-box-item">Wave n: '+ pulseListSorted[j] +'\n' +
            '                                 <button class="btn btn-warning btn list-view-box-btn" onclick=" goToWave('+
                pulseListSorted[j] + ',' + positionWhenAdd + ')">' +
                'Go</button>\n' +
            '                             </li>\n'
            }
        }
        else
        {

             for (var j= 0 ; j < pulses.length ; j++)
             {
            list_wave += '<li class="list-group-item list-view-box-item">Wave n: '+ pulses[j] +'\n' +
            '                                 <button class="btn btn-warning btn list-view-box-btn" onclick=" goToWave('+
                pulses[j] + ',' + positionWhenAdd + ')">' +
                'Go</button>\n' +
            '                             </li>\n'
             }
        }

        return  list_wave;

 }

