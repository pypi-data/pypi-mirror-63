#include "Webview.h"
#include "WebViewImpl.h"

WebViewImpl* Webview::m_webviewImpl = nullptr;

WebViewImpl* Webview::GetImpl()
{
	if (Webview::m_webviewImpl == nullptr)
	{
		Webview::m_webviewImpl = new WebViewImpl();
	}
	return Webview::m_webviewImpl;
}

Webview::Webview()
{
}

Webview::~Webview()
{
	delete m_webviewImpl;
	m_webviewImpl = nullptr;
}

void Webview::CreateWebView()
{
	GetImpl()->CreateWebView();
}

void Webview::RemoveWebView()
{
	GetImpl()->RemoveWebView();
}

void Webview::LoadURL(const char* url, bool cleanCache)
{
	GetImpl()->LoadURL(url, cleanCache);
}

void Webview::SetVisible(bool visible)
{
	GetImpl()->SetVisible(visible);
}

void Webview::SetRect(int left, int top, int maxWidth, int maxHeight)
{
	GetImpl()->SetRect(left, top, maxWidth, maxHeight);
}
