// renderer.js

document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const content = document.getElementById('content');

  // 서버 상태 표시 영역 동적 생성 (상단)
  const statusDiv = document.createElement('div');
  statusDiv.style.marginBottom = '20px';
  statusDiv.style.color = 'white';

  const statusHeader = document.createElement('h2');
  statusHeader.innerHTML = `서버 상태: <span id="server-status">확인 중...</span>`;
  statusDiv.appendChild(statusHeader);

  const apiListHeader = document.createElement('h3');
  apiListHeader.textContent = '사용 가능한 API 목록';
  statusDiv.appendChild(apiListHeader);

  const apiListUl = document.createElement('ul');
  apiListUl.id = 'api-list';
  statusDiv.appendChild(apiListUl);

  // 컨텐츠 영역 위에 상태 영역 추가
  content.parentNode.insertBefore(statusDiv, content);

  const statusSpan = statusDiv.querySelector('#server-status');

  // 메뉴 구성 (폴더 및 보드 항목)
  const menuData = [
    {
      folder: '폴더 A',
      boards: ['보드 1', '보드 2']
    },
    {
      folder: '폴더 B',
      boards: ['보드 3', '보드 4']
    },
    {
      folder: '폴더 C (3D)',
      boards: ['3D 그래프']
    },
    {
      folder: '폴더 D (실시간)',
      boards: ['실시간 그래프']
    }
  ];

  // 사이드바 메뉴 생성
  menuData.forEach(group => {
    const folderTitle = document.createElement('div');
    folderTitle.textContent = group.folder;
    folderTitle.style.marginTop = '10px';
    folderTitle.style.fontWeight = 'bold';
    folderTitle.style.color = 'white';
    sidebar.appendChild(folderTitle);

    group.boards.forEach(board => {
      const btn = document.createElement('div');
      btn.className = 'board-button';
      btn.textContent = board;
      btn.addEventListener('click', () => loadBoard(board));
      sidebar.appendChild(btn);
    });
  });

  // 서버 상태 업데이트 함수
  function updateServerStatus({ isUp, apiList }) {
    statusSpan.textContent = isUp ? '서버가 실행 중입니다.' : '서버가 실행되지 않았습니다.';
    updateApiList(apiList);
  }

  // API 목록 렌더링
  function updateApiList(apiList) {
    apiListUl.innerHTML = '';
    apiList.forEach(api => {
      const li = document.createElement('li');
      li.textContent = `${api.path} - ${api.description}`;
      li.style.color = 'white';
      apiListUl.appendChild(li);
    });
  }

  // 초기 서버 상태 요청
  window.electronAPI.getServerStatus()
    .then(updateServerStatus)
    .catch(() => {
      statusSpan.textContent = '서버 상태를 확인할 수 없습니다.';
    });

  // 서버 상태 실시간 업데이트 수신
  window.electronAPI.onServerStatusUpdate(updateServerStatus);

  // 보드 로딩 함수
  function loadBoard(boardName) {
    window.electronAPI.getBoardData(boardName)
      .then(data => {
        renderGraph(boardName, data);
      })
      .catch(() => {
        content.innerHTML = `<p style="color:red;">보드 데이터를 불러오는 데 실패했습니다.</p>`;
      });
  }

  // 그래프 렌더링 함수 (Chart.js 사용)
  function renderGraph(title, data) {
    content.innerHTML = `<h2>${title}</h2><canvas id="canvas"></canvas>`;

    if (data.type === '2d') {
      new Chart(document.getElementById('canvas'), {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: title,
            data: data.values,
            borderColor: 'cyan',
            tension: 0.3
          }]
        },
        options: {
          plugins: { legend: { labels: { color: 'white' } } },
          scales: {
            x: { ticks: { color: 'white' } },
            y: { ticks: { color: 'white' } }
          }
        }
      });
    } else if (data.type === '3d') {
      content.innerHTML += '<p style="color:white;">3D 그래프는 현재 Chart.js에서는 직접 지원되지 않지만, WebGL 또는 Python에서 렌더링된 이미지를 embed할 수 있습니다.</p>';
    } else if (data.type === 'realtime') {
      let phase = 0;
      const ctx = document.getElementById('canvas').getContext('2d');
      const realtimeChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: '실시간 사인파',
            data: data.values,
            borderColor: 'lime',
            tension: 0.3
          }]
        },
        options: {
          animation: false,
          plugins: { legend: { labels: { color: 'white' } } },
          scales: {
            x: { ticks: { color: 'white' } },
            y: { ticks: { color: 'white' } }
          }
        }
      });

      setInterval(() => {
        phase += 0.1;
        realtimeChart.data.datasets[0].data = data.labels.map(x => Math.sin(x + phase));
        realtimeChart.update();
      }, 50);
    }
  }

  // 초기 보드 로드
  loadBoard('보드 1');
});
