import React, { Component } from 'react';
import Chart from 'react-apexcharts'

var dates = [{x: '05/06/2014', y: 50},{x: '05/07/2014', y: 54},{x: '05/08/2014', y: 56},{x: '05/09/2014', y: 55}]

class ApexChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
      
        series: [{
          name: 'XYZ MOTORS',
          data: dates
        }],
        options: {
          chart: {
            type: 'area',
            stacked: false,
            height: 350,
            zoom: {
              type: 'x',
              enabled: true,
              autoScaleYaxis: true
            },
            toolbar: {
              autoSelected: 'zoom'
            }
          },
          annotations: {
            xaxis: [{
              x: new Date('08 May 2014').getTime(),
              x2: new Date('09 May 2014').getTime(),
              fillColor: '#B3F7CA',
              opacity: 0.4,
              label: {
                borderColor: '#B3F7CA',
                style: {
                  fontSize: '10px',
                  color: '#fff',
                  background: '#00E396',
                },
                offsetY: -10,
                text: 'Predicted Value',
              }
            }],
            points: [{
              x: new Date('09 May 2014').getTime(),
              y: 55,
              marker: {
                size: 8,
                fillColor: '#fff',
                strokeColor: 'red',
                radius: 2,
                cssClass: 'apexcharts-custom-class'
              },
              label: {
                borderColor: '#FF4560',
                offsetY: 0,
                style: {
                  color: '#fff',
                  background: '#FF4560',
                },
          
                text: 'Point Annotation',
              }
            }]
          },
          dataLabels: {
            enabled: false
          },
          markers: {
            size: 0,
          },
          title: {
            text: 'Stock Price Movement',
            align: 'left'
          },
          fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 1,
              inverseColors: false,
              opacityFrom: 0.5,
              opacityTo: 0,
              stops: [0, 90, 100]
            },
          },
          yaxis: {
            labels: {
              formatter: function (val) {
                return (val).toFixed(0);
              },
            },
            title: {
              text: 'Price'
            },
          },
          xaxis: {
            type: 'datetime',
          },
          tooltip: {
            shared: false,
            y: {
              formatter: function (val) {
                return (val).toFixed(0)
              }
            }
          }
        },
      
      
      };
    }

  

    render() {
      return (
  <div id="chart">
    <Chart options={this.state.options} series={this.state.series} type="area" height={350}></Chart>
</div>
      );
    }
}
export default ApexChart
  