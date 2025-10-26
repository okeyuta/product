document.addEventListener('DOMContentLoaded', function () {
  const toastContainer = document.getElementById('toast-container');

  function showToast(message, timeout = 2500) {
    if (!toastContainer) return;
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = message;
    toastContainer.appendChild(el);
    setTimeout(() => {
      el.classList.add('hide');
      setTimeout(() => el.remove(), 400);
    }, timeout);
  }

  // Style anchors with role "botton"
  document
    .querySelectorAll('a[role="botton"]')
    .forEach((a) => a.classList.add('btn'));

  // Handle regist form via fetch + simple validation
  const registForm = document.getElementById('regist-form');
  if (registForm) {
    registForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = registForm
        .querySelector('input[name="title"]')
        .value.trim();
      if (!title) {
        showToast('タイトルは必須です');
        return;
      }
      const formData = new FormData(registForm);
      try {
        const res = await fetch(registForm.action || window.location.href, {
          method: 'POST',
          body: formData,
          credentials: 'same-origin',
        });
        if (res.status === 200 || res.status === 302 || res.redirected) {
          showToast('登録しました');
          // small delay for toast visibility
          setTimeout(() => (window.location.href = '/'), 500);
        } else {
          showToast('登録に失敗しました');
        }
      } catch (err) {
        showToast('ネットワークエラー');
      }
    });
  }

  // AJAX delete from index page
  document.querySelectorAll('a.js-delete').forEach((a) => {
    a.addEventListener('click', async (e) => {
      e.preventDefault();
      if (!confirm('このメモを削除しますか？')) return;
      const href = a.getAttribute('href');
      try {
        const res = await fetch(href, {
          method: 'POST',
          credentials: 'same-origin',
        });
        if (res.status === 200 || res.status === 302) {
          const tr = a.closest('tr');
          if (tr) tr.remove();
          showToast('削除しました');
        } else {
          showToast('削除に失敗しました');
        }
      } catch (err) {
        showToast('ネットワークエラー');
      }
    });
  });

  // Simple enhancement: confirm delete on delete form page
  const deleteForm = document.getElementById('delete-form');
  if (deleteForm) {
    deleteForm.addEventListener('submit', function (e) {
      if (!confirm('このメモを削除しますか？')) {
        e.preventDefault();
      }
    });
  }

  // Small usability: focus first input on pages with a form
  const firstInput = document.querySelector('form input[type="text"]');
  if (firstInput) firstInput.focus();
});
