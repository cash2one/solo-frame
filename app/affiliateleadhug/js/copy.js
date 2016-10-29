var clipboard = new Clipboard('.copy');
clipboard.on('success', function(e) {
    console.log('copied!');
});
clipboard.on('error', function(e) {
    console.log('copy failed!');
});
