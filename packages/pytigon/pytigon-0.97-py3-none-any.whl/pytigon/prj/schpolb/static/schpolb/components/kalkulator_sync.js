// Transcrypt'ed from Python, 2020-02-23 20:53:14
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var _sync_elem = function (resolve, reject) {
	var props = ['rec'];
	var data = function () {
		return dict ({'status': 0});
	};
	var template = '<div>xxx{{status}}yyy</div>';
	var mounted = function () {
		var vue_obj = this;
		console.log ('X1');
		var on_open_database = function (db) {
			console.log ('X2');
			var complete = function (responseText, table_name) {
				var x = JSON.parse (responseText);
				vue_obj.status = vue_obj.status + 1;
				console.log ('Success opening DB');
				var tabObjectStore = db.transaction (table_name, 'readwrite').objectStore (table_name);
				var clear_request = tabObjectStore.clear ();
				var _clearsuccess = function (event) {
					for (var pos of x) {
						if (table_name == 'kar') {
							var obj = dict ({'symkar': pos [4], 'path': pos [0], 'pathopis': pos [1], 'grupa': pos [2], 'opisgrupy': pos [3], 'opikar': pos [5]});
						}
						if (table_name == 'mag') {
							var obj = dict ({'mag': pos [0], 'opismag': pos [1], 'symodd': pos [2]});
						}
						if (table_name == 'tkw') {
							var obj = dict ({'symkary': pos [0], 'sur': pos [1], 'rob': pos [2], 'adm': pos [3], 'zmien': pos [4], 'amort': pos [5], 'kosztmag': pos [6]});
						}
						if (table_name == 'przel') {
							var obj = dict ({'symkar': pos [0], 'waga': pos [1], 'mprzel': pos [2]});
						}
						tabObjectStore.add (obj);
					}
				};
				clear_request.onsuccess = _clearsuccess;
			};
			var _complete = function (table_name) {
				var _complete2 = function (responseText) {
					return complete (responseText, table_name);
				};
				return _complete2;
			};
			ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/0/', _complete ('kar'));
			ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/1/', _complete ('mag'));
			ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/2/', _complete ('tkw'));
			ajax_get (BASE_PATH + '/sprzedaz/kalkulator_tables/3/', _complete ('przel'));
		};
		open_database (on_open_database);
	};
	resolve (dict ({'data': data, 'template': template, 'mounted': mounted}));
};
Vue.component ('sync_elem', _sync_elem);

//# sourceMappingURL=input.map