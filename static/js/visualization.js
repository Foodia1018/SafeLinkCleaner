/**
 * SafeLink Protection Cleaner - Data Visualization Module
 * Creates charts and visualizations for the application using D3.js
 */

// Initialize visualizations when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeVisualizations();
});

/**
 * Initialize all visualizations
 */
function initializeVisualizations() {
    // Initialize charts based on available chart containers
    if (document.getElementById('security-systems-chart')) {
        initSecuritySystemsChart();
    }
    
    if (document.getElementById('domain-distribution-chart')) {
        initDomainDistributionChart();
    }
    
    if (document.getElementById('processing-history-chart')) {
        initProcessingHistoryChart();
    }
    
    if (document.getElementById('removal-rate-gauge')) {
        initRemovalRateGauge();
    }
}

/**
 * Initialize security systems chart
 */
function initSecuritySystemsChart() {
    const chartContainer = document.getElementById('security-systems-chart');
    const dataElement = document.getElementById('security-systems-data');
    
    if (!chartContainer || !dataElement) return;
    
    try {
        const data = JSON.parse(dataElement.textContent);
        
        if (!data || !data.length) {
            chartContainer.innerHTML = '<div class="text-center text-muted">No security systems detected</div>';
            return;
        }
        
        // Sort data by count in descending order
        const sortedData = [...data].sort((a, b) => b.count - a.count);
        
        // Set up dimensions
        const width = chartContainer.clientWidth;
        const height = 300;
        const margin = { top: 20, right: 30, bottom: 90, left: 60 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        // Create SVG
        const svg = d3.select(chartContainer)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Create chart group
        const chart = svg.append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);
        
        // Set up scales
        const xScale = d3.scaleBand()
            .domain(sortedData.map(d => d.name))
            .range([0, innerWidth])
            .padding(0.2);
        
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(sortedData, d => d.count) * 1.1])
            .range([innerHeight, 0]);
        
        // Create color scale
        const colorScale = d3.scaleOrdinal()
            .domain(sortedData.map(d => d.name))
            .range(d3.schemeBlues[9]);
        
        // Add X axis
        chart.append('g')
            .attr('transform', `translate(0, ${innerHeight})`)
            .call(d3.axisBottom(xScale))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .style('font-size', '12px')
            .style('fill', '#b0b0b0');
        
        // Add Y axis
        chart.append('g')
            .call(d3.axisLeft(yScale))
            .selectAll('text')
            .style('font-size', '12px')
            .style('fill', '#b0b0b0');
        
        // Add Y axis label
        chart.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', -50)
            .attr('x', -innerHeight / 2)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('fill', '#ffffff')
            .text('Number of Emails');
        
        // Add bars
        chart.selectAll('.bar')
            .data(sortedData)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', d => xScale(d.name))
            .attr('width', xScale.bandwidth())
            .attr('y', d => yScale(d.count))
            .attr('height', d => innerHeight - yScale(d.count))
            .attr('fill', d => colorScale(d.name))
            .attr('rx', 3) // Rounded corners
            .attr('ry', 3)
            .on('mouseover', function(event, d) {
                d3.select(this).attr('fill', d3.color(colorScale(d.name)).brighter(0.5));
                
                // Show tooltip
                const tooltip = d3.select(chartContainer).append('div')
                    .attr('class', 'chart-tooltip')
                    .style('position', 'absolute')
                    .style('background-color', 'rgba(30, 30, 30, 0.9)')
                    .style('color', '#ffffff')
                    .style('padding', '8px')
                    .style('border-radius', '4px')
                    .style('font-size', '12px')
                    .style('pointer-events', 'none')
                    .style('z-index', 1000)
                    .style('left', `${event.pageX - chartContainer.getBoundingClientRect().left}px`)
                    .style('top', `${event.pageY - chartContainer.getBoundingClientRect().top - 40}px`);
                
                tooltip.html(`<strong>${d.name}</strong>: ${d.count} emails`);
            })
            .on('mouseout', function(event, d) {
                d3.select(this).attr('fill', colorScale(d.name));
                d3.select(chartContainer).selectAll('.chart-tooltip').remove();
            });
            
        // Add value labels on top of bars
        chart.selectAll('.label')
            .data(sortedData)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('x', d => xScale(d.name) + xScale.bandwidth() / 2)
            .attr('y', d => yScale(d.count) - 5)
            .attr('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('fill', '#ffffff')
            .text(d => d.count);
        
    } catch (error) {
        console.error('Error initializing security systems chart:', error);
        chartContainer.innerHTML = '<div class="alert alert-danger">Error loading chart data</div>';
    }
}

/**
 * Initialize domain distribution chart
 */
function initDomainDistributionChart() {
    const chartContainer = document.getElementById('domain-distribution-chart');
    const dataElement = document.getElementById('domain-distribution-data');
    
    if (!chartContainer || !dataElement) return;
    
    try {
        const data = JSON.parse(dataElement.textContent);
        
        if (!data || !data.length) {
            chartContainer.innerHTML = '<div class="text-center text-muted">No domain data available</div>';
            return;
        }
        
        // Sort data by count in descending order
        const sortedData = [...data].sort((a, b) => b.count - a.count);
        
        // Use only top 10 domains if more are available
        const chartData = sortedData.slice(0, 10);
        const totalEmails = sortedData.reduce((acc, curr) => acc + curr.count, 0);
        
        // Set up dimensions
        const width = chartContainer.clientWidth;
        const height = 300;
        
        // Create SVG
        const svg = d3.select(chartContainer)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);
        
        // Set up pie chart
        const radius = Math.min(width, height) / 2 - 40;
        
        const pie = d3.pie()
            .value(d => d.count)
            .sort(null);
        
        const arc = d3.arc()
            .innerRadius(radius * 0.5) // Donut chart
            .outerRadius(radius);
        
        // Create color scale
        const colorScale = d3.scaleOrdinal()
            .domain(chartData.map(d => d.domain))
            .range(d3.schemeGreenBlue[9]);
        
        // Add arcs
        const arcs = svg.selectAll('.arc')
            .data(pie(chartData))
            .enter()
            .append('g')
            .attr('class', 'arc');
        
        arcs.append('path')
            .attr('d', arc)
            .attr('fill', d => colorScale(d.data.domain))
            .attr('stroke', '#252525')
            .style('stroke-width', '1px')
            .on('mouseover', function(event, d) {
                d3.select(this).attr('fill', d3.color(colorScale(d.data.domain)).brighter(0.5));
                
                // Show tooltip
                const tooltip = d3.select(chartContainer).append('div')
                    .attr('class', 'chart-tooltip')
                    .style('position', 'absolute')
                    .style('background-color', 'rgba(30, 30, 30, 0.9)')
                    .style('color', '#ffffff')
                    .style('padding', '8px')
                    .style('border-radius', '4px')
                    .style('font-size', '12px')
                    .style('pointer-events', 'none')
                    .style('z-index', 1000)
                    .style('left', `${event.pageX - chartContainer.getBoundingClientRect().left}px`)
                    .style('top', `${event.pageY - chartContainer.getBoundingClientRect().top - 40}px`);
                
                const percentage = ((d.data.count / totalEmails) * 100).toFixed(1);
                tooltip.html(`<strong>${d.data.domain}</strong>: ${d.data.count} emails (${percentage}%)`);
            })
            .on('mouseout', function(event, d) {
                d3.select(this).attr('fill', colorScale(d.data.domain));
                d3.select(chartContainer).selectAll('.chart-tooltip').remove();
            });
        
        // Add center text
        svg.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '.35em')
            .style('font-size', '14px')
            .style('fill', '#ffffff')
            .text(`${totalEmails} Emails`);
        
        // Add legend
        const legendGroup = svg.append('g')
            .attr('transform', `translate(${radius + 20}, ${-radius})`);
        
        chartData.forEach((d, i) => {
            const legendRow = legendGroup.append('g')
                .attr('transform', `translate(0, ${i * 20})`);
            
            legendRow.append('rect')
                .attr('width', 10)
                .attr('height', 10)
                .attr('fill', colorScale(d.domain));
            
            legendRow.append('text')
                .attr('x', 15)
                .attr('y', 10)
                .text(d.domain)
                .style('font-size', '12px')
                .style('fill', '#b0b0b0');
        });
        
    } catch (error) {
        console.error('Error initializing domain distribution chart:', error);
        chartContainer.innerHTML = '<div class="alert alert-danger">Error loading chart data</div>';
    }
}

/**
 * Initialize processing history chart
 */
function initProcessingHistoryChart() {
    const chartContainer = document.getElementById('processing-history-chart');
    const dataElement = document.getElementById('processing-history-data');
    
    if (!chartContainer || !dataElement) return;
    
    try {
        const data = JSON.parse(dataElement.textContent);
        
        if (!data || !data.length) {
            chartContainer.innerHTML = '<div class="text-center text-muted">No processing history available</div>';
            return;
        }
        
        // Set up dimensions
        const width = chartContainer.clientWidth;
        const height = 300;
        const margin = { top: 20, right: 30, bottom: 50, left: 60 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        // Create SVG
        const svg = d3.select(chartContainer)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Create chart group
        const chart = svg.append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);
        
        // Set up scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, d => new Date(d.date)))
            .range([0, innerWidth]);
        
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => Math.max(d.original, d.cleaned)) * 1.1])
            .range([innerHeight, 0]);
        
        // Add X axis
        chart.append('g')
            .attr('transform', `translate(0, ${innerHeight})`)
            .call(d3.axisBottom(xScale).ticks(5).tickFormat(d3.timeFormat('%b %d')))
            .selectAll('text')
            .style('font-size', '12px')
            .style('fill', '#b0b0b0');
        
        // Add Y axis
        chart.append('g')
            .call(d3.axisLeft(yScale))
            .selectAll('text')
            .style('font-size', '12px')
            .style('fill', '#b0b0b0');
        
        // Add Y axis label
        chart.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', -50)
            .attr('x', -innerHeight / 2)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('fill', '#ffffff')
            .text('Number of Emails');
        
        // Create line generators
        const originalLine = d3.line()
            .x(d => xScale(new Date(d.date)))
            .y(d => yScale(d.original));
        
        const cleanedLine = d3.line()
            .x(d => xScale(new Date(d.date)))
            .y(d => yScale(d.cleaned));
        
        // Add original emails line
        chart.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', '#2196f3')
            .attr('stroke-width', 2)
            .attr('d', originalLine);
        
        // Add cleaned emails line
        chart.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', '#4caf50')
            .attr('stroke-width', 2)
            .attr('d', cleanedLine);
        
        // Add legend
        const legend = chart.append('g')
            .attr('transform', `translate(${innerWidth - 150}, 0)`);
        
        // Original emails legend
        legend.append('rect')
            .attr('width', 15)
            .attr('height', 3)
            .attr('fill', '#2196f3');
        
        legend.append('text')
            .attr('x', 20)
            .attr('y', 5)
            .text('Original Emails')
            .style('font-size', '12px')
            .style('fill', '#b0b0b0');
        
        // Cleaned emails legend
        legend.append('rect')
            .attr('width', 15)
            .attr('height', 3)
            .attr('y', 15)
            .attr('fill', '#4caf50');
        
        legend.append('text')
            .attr('x', 20)
            .attr('y', 20)
            .text('Cleaned Emails')
            .style('font-size', '12px')
            .style('fill', '#b0b0b0');
        
    } catch (error) {
        console.error('Error initializing processing history chart:', error);
        chartContainer.innerHTML = '<div class="alert alert-danger">Error loading chart data</div>';
    }
}

/**
 * Initialize removal rate gauge
 */
function initRemovalRateGauge() {
    const gaugeContainer = document.getElementById('removal-rate-gauge');
    
    if (!gaugeContainer) return;
    
    try {
        // Get the removal rate from data attribute
        const removalRate = parseFloat(gaugeContainer.dataset.rate || 0);
        
        // Set up dimensions
        const width = gaugeContainer.clientWidth;
        const height = 200;
        const margin = { top: 20, right: 30, bottom: 30, left: 30 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        // Create SVG
        const svg = d3.select(gaugeContainer)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Create gauge group
        const gauge = svg.append('g')
            .attr('transform', `translate(${width / 2}, ${height - 30})`);
        
        // Set up gauge parameters
        const radius = Math.min(innerWidth, innerHeight) / 2;
        const startAngle = -Math.PI / 2;
        const endAngle = Math.PI / 2;
        
        // Create arc generator
        const arc = d3.arc()
            .innerRadius(radius * 0.7)
            .outerRadius(radius)
            .startAngle(startAngle)
            .endAngle(endAngle);
        
        // Create background arc
        gauge.append('path')
            .attr('d', arc)
            .style('fill', '#333333');
        
        // Create foreground arc based on removal rate
        const foregroundArc = d3.arc()
            .innerRadius(radius * 0.7)
            .outerRadius(radius)
            .startAngle(startAngle)
            .endAngle(startAngle + (endAngle - startAngle) * (removalRate / 100));
        
        // Determine color based on removal rate
        let color;
        if (removalRate < 30) {
            color = '#4caf50'; // Green for low removal rate
        } else if (removalRate < 70) {
            color = '#ff9800'; // Orange for medium removal rate
        } else {
            color = '#f44336'; // Red for high removal rate
        }
        
        gauge.append('path')
            .attr('d', foregroundArc)
            .style('fill', color);
        
        // Add gauge value text
        gauge.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', -20)
            .style('font-size', '28px')
            .style('font-weight', '300')
            .style('fill', '#ffffff')
            .text(`${removalRate.toFixed(1)}%`);
        
        gauge.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', 10)
            .style('font-size', '14px')
            .style('fill', '#b0b0b0')
            .text('Removal Rate');
        
        // Add tick marks
        const tickData = [0, 25, 50, 75, 100];
        const tickScale = d3.scaleLinear()
            .domain([0, 100])
            .range([startAngle, endAngle]);
        
        tickData.forEach(tick => {
            const tickAngle = tickScale(tick);
            const tickX = Math.cos(tickAngle) * (radius + 10);
            const tickY = Math.sin(tickAngle) * (radius + 10);
            
            // Add tick line
            gauge.append('line')
                .attr('x1', Math.cos(tickAngle) * radius)
                .attr('y1', Math.sin(tickAngle) * radius)
                .attr('x2', tickX)
                .attr('y2', tickY)
                .style('stroke', '#666666')
                .style('stroke-width', 1);
            
            // Add tick label
            gauge.append('text')
                .attr('x', Math.cos(tickAngle) * (radius + 20))
                .attr('y', Math.sin(tickAngle) * (radius + 20))
                .attr('text-anchor', 'middle')
                .style('font-size', '12px')
                .style('fill', '#b0b0b0')
                .text(tick + '%');
        });
        
    } catch (error) {
        console.error('Error initializing removal rate gauge:', error);
        gaugeContainer.innerHTML = '<div class="alert alert-danger">Error loading gauge data</div>';
    }
}
