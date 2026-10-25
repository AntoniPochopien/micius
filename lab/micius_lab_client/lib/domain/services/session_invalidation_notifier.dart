import 'dart:async';

import 'package:injectable/injectable.dart';

@Singleton()
class SessionInvalidationNotifier {
  final _controller = StreamController<void>.broadcast();

  Stream<void> get stream => _controller.stream;

  void notifySessionInvalidated() {
    if (!_controller.isClosed) {
      _controller.add(null);
    }
  }
}
