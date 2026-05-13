try {
    const fs = require('fs');
    const content = fs.readFileSync('index.html', 'utf8');
    const scriptMatch = content.match(/<script>([\s\S]*?)<\/script>/);
    if (!scriptMatch) {
        console.error("No script tag found");
        process.exit(1);
    }
    const script = scriptMatch[1];

    // Mock browser environment
    const window = {
        addEventListener: () => {},
        location: { hash: '', search: '' },
        history: { replaceState: () => {} },
        scrollTo: () => {}
    };
    const document = {
        documentElement: { classList: { add: () => {}, remove: () => {} } },
        querySelectorAll: () => [],
        getElementById: () => ({ addEventListener: () => {} }),
        body: { classList: { toggle: () => {}, contains: () => false } }
    };
    const localStorage = { getItem: () => null, setItem: () => {} };
    const navigator = { language: 'pl' };
    const Image = function() {};
    const alert = () => {};

    const sandbox = { window, document, localStorage, navigator, console, Image, alert };
    const fn = new Function('window', 'document', 'localStorage', 'navigator', 'console', 'Image', 'alert', script + '\nreturn translations;');
    const translations = fn(window, document, localStorage, navigator, console, Image, alert);

    console.log("Syntax OK");
    console.log("Langs in translations:", Object.keys(translations).join(', '));
} catch (e) {
    console.error("Syntax Error:", e);
    process.exit(1);
}
