import Plotly from 'plotly.js-dist-min';

// json 데이터 파싱 함수
function parseJSON(dataStr) {
  try {
    return JSON.parse(dataStr);
  } catch (e) {
    alert('JSON 파싱 오류');
    return null;
  }
}

// csv -> 배열 변환 간단 함수
function parseCSV(dataStr) {
  const lines = dataStr.trim().split('\n');
  const headers = lines[0].split(',');
  const rows = lines.slice(1).map(line => {
    const values = line.split(',');
    let obj = {};
    headers.forEach((h, i) => obj[h.trim()] = values[i].trim());
    return obj;
  });
  return rows;
}

document.getElementById('loadBtn').addEventListener('click', () => {
  const fileName = document.getElementById('fileSelector').value;
  const rawData = window.electronAPI.readDataFile(fileName);

  if (!rawData) {
    alert('파일을 읽을 수 없습니다.');
    return;
  }

  let data;
  if (fileName.endsWith('.json')) {
    data = parseJSON(rawData);
  } else if (fileName.endsWith('.csv')) {
    data = parseCSV(rawData);
  } else {
    alert('지원하지 않는 파일 형식입니다.');
    return;
  }

  if (!data) return;

  // 간단히 x, y 추출 (예: year, value)
  // 파일에 맞게 필드명 조정 필요
  let x = [];
  let y = [];

  if (Array.isArray(data)) {
    // CSV or JSON 배열 형태
    data.forEach(item => {
      x.push(item.year || item.Year);
      y.push(parseFloat(item.value || item.Value));
    });
  } else {
    alert('데이터 구조가 올바르지 않습니다.');
    return;
  }

  const trace = {
    x,
    y,
    type: 'scatter',
    mode: 'lines+markers',
    marker: { color: 'blue' },
  };

  Plotly.newPlot('plot', [trace], {
    margin: { t: 20 },
    title: '데이터 시각화 예제',
  });
});
